import React from 'react';
import { Audio, Series, Sequence, staticFile } from 'remotion';
import { ProjectData, SceneData } from './types';
import { Background } from './components/Background';
import { TitleCard } from './components/TitleCard';
import { CodeExplainer } from './components/CodeExplainer';
import { ArchitectureFlow } from './components/ArchitectureFlow';
import { MathVisualizer } from './components/MathVisualizer';
import { ComparisonCard } from './components/ComparisonCard';
import { SummaryList } from './components/SummaryList';
import { OutroCard } from './components/OutroCard';
import { TerminalSplit } from './components/TerminalSplit';
import { ClassifierCard } from './components/ClassifierCard';
import { ClusterGrid } from './components/ClusterGrid';
import { SubtitleOverlay } from './components/SubtitleOverlay';
import { getTheme } from './theme';
import { ManimClip } from './components/ManimClip';
import { TypingCode } from './components/TypingCode';
import { TerminalRun } from './components/TerminalRun';
import { BrowserSteps } from './components/BrowserSteps';
import { ArrayViz } from './components/ArrayViz';
import { TreeViz } from './components/TreeViz';
import { GraphViz } from './components/GraphViz';
import { StackQueueViz } from './components/StackQueueViz';
import { DiagramFlow } from './components/DiagramFlow';
import { TeacherTip } from './components/TeacherTip';
import { StatChart } from './components/StatChart';
import { ThemeProvider } from './ThemeContext';
import { Camera } from './components/Camera';
import { SceneFade, GlobalProgress, useTotalFrames, KeyIdea, ChapterLabel } from './components/SceneFx';

export const VideoComposition: React.FC<{ project: ProjectData }> = ({ project }) => {
  const { scenes, aspectRatio } = project;
  const theme = getTheme(project.theme);

  const renderSceneContent = (scene: SceneData) => {
    switch (scene.type) {
      case 'TitleCard':
        return <TitleCard {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'CodeExplainer':
        return <CodeExplainer {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'ArchitectureFlow':
        return <ArchitectureFlow {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'MathVisualizer':
        return <MathVisualizer {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'ComparisonCard':
        return <ComparisonCard {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'TypingCode': {
        const p = scene.props as any;
        const tf = p.typeFrames ?? Math.round((scene.durationInFrames || 90) * 0.8);
        return <TypingCode {...p} typeFrames={tf} />;
      }
      case 'TerminalRun': {
        const p = scene.props as any;
        const tf = p.typeFrames ?? Math.round((scene.durationInFrames || 90) * 0.3);
        return <TerminalRun {...p} typeFrames={tf} />;
      }
      case 'StatChart': {
        const p = scene.props as any;
        const tf = p.typeFrames ?? Math.round((scene.durationInFrames || 90) * 0.7);
        return <StatChart {...p} typeFrames={tf} />;
      }
      case 'ManimClip':
        return <ManimClip {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'SummaryList':
        return <SummaryList {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'OutroCard':
        return <OutroCard {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'TerminalSplit':
        return <TerminalSplit {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'ClassifierCard':
        return <ClassifierCard {...(scene.props as any)} aspectRatio={aspectRatio} />;
      case 'BrowserSteps':
        return <BrowserSteps {...(scene.props as any)} stepAt={(scene as any).stepAt} aspectRatio={aspectRatio} />;
      case 'ArrayViz':
        return <ArrayViz {...(scene.props as any)} stepAt={(scene as any).stepAt} aspectRatio={aspectRatio} />;
      case 'TreeViz':
        return <TreeViz {...(scene.props as any)} stepAt={(scene as any).stepAt} aspectRatio={aspectRatio} />;
      case 'GraphViz':
        return <GraphViz {...(scene.props as any)} stepAt={(scene as any).stepAt} aspectRatio={aspectRatio} />;
      case 'DiagramFlow':
        return <DiagramFlow {...(scene.props as any)} stepAt={(scene as any).stepAt} aspectRatio={aspectRatio} />;
      case 'StackQueueViz':
        return <StackQueueViz {...(scene.props as any)} stepAt={(scene as any).stepAt} aspectRatio={aspectRatio} />;
      case 'ClusterGrid':
        return <ClusterGrid {...(scene.props as any)} aspectRatio={aspectRatio} />;
      default:
        return null;
    }
  };

  return (
    <ThemeProvider name={project.theme}>
    <div className="w-full h-full relative overflow-hidden font-sans select-none" style={{ color: theme.text }}>
      {/* Dynamic Background */}
      <Background aspectRatio={aspectRatio} theme={project.theme} />

      {/* Sequential Scenes */}
      <Series>
        {scenes.map((scene) => {
          const duration = scene.durationInFrames || 90;

          return (
            <Series.Sequence key={scene.id} durationInFrames={duration}>
              {/* Scene Visual */}
              <div className="w-full h-full relative z-10">
                <SceneFade>
                  <Camera keys={(scene as any).camera} aspectRatio={aspectRatio}>
                    {renderSceneContent(scene)}
                  </Camera>
                </SceneFade>
                {(scene as any).chapter && <ChapterLabel text={(scene as any).chapter} />}
                {(scene as any).keyIdea && <KeyIdea text={(scene as any).keyIdea} />}
              </div>

              {/* Sound: typing loop (code scenes) */}
              {scene.type === 'TypingCode' && (scene as any).keysFile && (
                <Audio src={staticFile((scene as any).keysFile)} volume={0.9} />
              )}
              {scene.type === 'TypingCode' && !(scene as any).keysFile && (
                <Audio src={staticFile('sfx/typing.wav')} loop volume={0.35} />
              )}
              {/* Sound: har popup par pop */}
              {((scene as any).popups || []).map((pp: any, pi: number) => (
                <Sequence key={`pop${pi}`} from={Math.round((pp.at || 0) * 30)} layout="none">
                  <Audio src={staticFile('sfx/pop.wav')} volume={0.5} />
                </Sequence>
              ))}
              {/* Teacher popups (scene ke andar, sec ke hisaab se) */}
              {((scene as any).popups || []).map((pp: any, pi: number) => (
                <TeacherTip key={pi} text={pp.text} kind={pp.kind} x={pp.x} y={pp.y}
                  startFrame={Math.round((pp.at || 0) * 30)} hideAfter={pp.hideAfter ? Math.round(pp.hideAfter * 30) : undefined} />
              ))}

              {/* Subtitles Overlay */}
              <SubtitleOverlay
                words={scene.words}
                aspectRatio={aspectRatio}
                narrationFallback={scene.narration}
              />

              {/* Scene Voiceover Audio */}
              {scene.audioFile && (
                <Audio src={staticFile(scene.audioFile)} />
              )}
            </Series.Sequence>
          );
        })}
      </Series>

      {/* Top progress bar (poori video ka progress) */}
      <GlobalProgress totalFrames={useTotalFrames(scenes)} />

      {/* Background music (poori video mein, low volume) */}
      <Audio src={staticFile((project as any).bgm || 'sfx/bgm.wav')} loop volume={(project as any).bgmVolume ?? 0.08} />

      {/* Progress footer, reference style: "Progress • Day N/30" */}
      {project.dayLabel && (
        <div className="absolute left-0 right-0 bottom-3 flex justify-center pointer-events-none z-50">
          <div className="font-mono text-base" style={{ color: theme.textMuted }}>Progress • {project.dayLabel}</div>
        </div>
      )}
    </div>
    </ThemeProvider>
  );
};
