import subprocess, torch, sys
print("=== GPU CHECK ===")
print(subprocess.run(['nvidia-smi','--query-gpu=name,memory.total','--format=csv'],capture_output=True,text=True).stdout)
print("torch:", torch.__version__, "| cuda:", torch.cuda.is_available(), "| devices:", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(f"GPU{i}:", torch.cuda.get_device_name(i))
print("=== SETUP CHECK PASSED ===")
