# Profiling with Scalene

Scalene 2.x splits profiling into two commands. `--html` belongs to `view`, not `run`.

```bash
python3 -m scalene run script.py            # writes scalene-profile.json
python3 -m scalene view --standalone        # one self-contained scalene-profile.html
python3 -m scalene view --cli -r            # in the terminal, only active lines
```

- Use `--standalone`. Plain `--html` writes a page that loads other files and can render blank when opened from disk.
- `run --cpu-only` is faster. `-o name.json` names the profile file.
- Async work shows up as `[await] ...` entries.
- A script that mostly sleeps gives a sparse profile: Scalene samples what the Python code is doing.

The files here are a profile of `01_concurrency_basics/concurrent_sleep.py`.
