# Counter Logs to AWS CloudWatch with Docker

## Installation

```bash
poetry install
```

# Run example

```bash
python main.py --docker-image python --bash-command $'pip install pip -U && pip install tqdm && python -c \"import time\ncounter = 0\nwhile True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"'--aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1--aws-access-key-id ... --aws-secret-access-key ... --aws-region ...
```

or

```bash
docker-to-cloudwatch --docker-image python --bash-command $'pip install pip -U && pip install tqdm && python -c \"import time\ncounter = 0\nwhile True:\n\tprint(counter)\n\tcounter = counter + 1\n\ttime.sleep(0.1)\"'--aws-cloudwatch-group test-task-group-1 --aws-cloudwatch-stream test-task-stream-1--aws-access-key-id ... --aws-secret-access-key ... --aws-region ...
```

## Help

```bash
python main.py --help
```

## Tests

don't think 4 hours is enough to write tests as well, but if I would test it:

- For stdin tests I would use
  pytest's [capsys fixture](https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html)
- Could use [moto](https://docs.getmoto.org/en/latest/docs/getting_started.html) for testing clouldwatch operations (but
  it seems the SequenceToken is not supported yet: https://docs.getmoto.org/en/latest/docs/services/logs.html)
- For testing docker nothing extra is required, maximum is a change `DOCKER_HOST` if you want to use a another docker
  daemon for testing

## Shell Completion

Since we have click for cli we can add shell completion as well if you need it:
[How to install it](https://click.palletsprojects.com/en/8.1.x/shell-completion/)
