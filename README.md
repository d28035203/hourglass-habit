# Hourglass Habit

CLI logger for daily hours by subject. Stores rows in a local CSV (`hours.csv`).

## Usage

```bash
python3 log.py add backend 2.5 "auth middleware"
python3 log.py add algorithms 1.0
python3 log.py today
python3 log.py summary
```

Override the log path with `HOURGLASS_LOG`.

## License

MIT
