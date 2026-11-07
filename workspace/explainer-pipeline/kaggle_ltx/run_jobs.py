"""Sandbox-se-control LTX pipeline. Use:
  1) ~/.kaggle/kaggle.json rakho (user dega)
  2) python run_jobs.py jobs_dir/   (jobs_dir: jobs.json + scene images)
Flow: dataset push -> kernel push (GPU) -> poll -> output mp4s download -> /var/tmp/ltx_out/
"""
import json, os, subprocess, sys, time, shutil
KDIR=os.path.dirname(os.path.abspath(__file__))
def sh(c): print("+",c); return subprocess.run(c,shell=True,capture_output=True,text=True)
def main(jobdir):
    u=json.load(open(os.path.expanduser('~/.kaggle/kaggle.json')))['username']
    ds=f"{u}/ltx-jobs-input"; kn=f"{u}/ltx-worker-auto"
    # dataset (inputs)
    meta={"title":"ltx-jobs-input","id":ds,"licenses":[{"name":"CC0-1.0"}]}
    json.dump(meta,open(os.path.join(jobdir,'dataset-metadata.json'),'w'))
    r=sh(f"kaggle datasets create -p {jobdir} --dir-mode zip") 
    if 'already exists' in r.stdout+r.stderr: sh(f"kaggle datasets version -p {jobdir} -m update --dir-mode zip")
    time.sleep(20)
    # kernel (GPU worker)
    kd=os.path.join(KDIR,'kernel')
    json.dump({"id":kn,"title":"ltx-worker-auto","code_file":"ltx_worker.py","language":"python",
               "kernel_type":"script","is_private":True,"enable_gpu":True,"enable_internet":True,
               "dataset_sources":[ds],"kernel_sources":[],"competition_sources":[]},
              open(os.path.join(kd,'kernel-metadata.json'),'w'))
    sh(f"kaggle kernels push -p {kd}")
    # poll
    while True:
        time.sleep(60)
        st=sh(f"kaggle kernels status {kn}").stdout
        print(st.strip())
        if 'complete' in st: break
        if 'error' in st: print(sh(f"kaggle kernels output {kn} -p /var/tmp/ltx_out").stdout); sys.exit(1)
    os.makedirs('/var/tmp/ltx_out',exist_ok=True)
    sh(f"kaggle kernels output {kn} -p /var/tmp/ltx_out")
    print("CLIPS:", os.listdir('/var/tmp/ltx_out'))
if __name__=="__main__": main(sys.argv[1])
