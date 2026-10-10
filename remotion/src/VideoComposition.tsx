import React from 'react';
import { Audio, Series, staticFile } from 'remotion';
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
import { ThemeProvider } from './ThemeContext';

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
                {renderSceneContent(scene)}
              </div>

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
    </div>
    </ThemeProvider>
  );
};
