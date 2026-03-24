# Port Scanner
An asynchronous network scanning tool that performs port scanning, service detection, banner grabbing developed in python.

## Features
- Asynchronous port scanning using `asyncio`
- Different scanning options including full scan (1-65536) or scan of commonly known ports
- Banner grabbing for open ports
- JSON output for scan results


## How to use
```bash
git clone https://github.com/mlchandran23/port-scanner.git
cd port-scanner
python port_scanner.py
```

results will be saved in the `output/` directory as JSON files