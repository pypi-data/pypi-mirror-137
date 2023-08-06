import hek

# process name
name = "chrome.exe"

# kill process
res = hek.system.process.kill_process(name=name)

print(res)