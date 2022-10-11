# `tap-checkly`

Singer tap for Checkly.

Built with the [Meltano SDK](https://sdk.meltano.com) for Singer Taps and Targets.

## Capabilities

* `catalog`
* `state`
* `discover`
* `about`
* `stream-maps`
* `schema-flattening`

## Settings

| Setting             | Required | Default | Description                                                                   |
|:--------------------|:--------:|:-------:|:------------------------------------------------------------------------------|
| account_id          | True     | None    | Checkly Account ID                                                            |
| token               | True     | None    | API Token for Checkly                                                         |
| start_date          | False    | None    | Earliest datetime to get data from                                            |
| stream_maps         | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config   | False    | None    | User-defined config values to be used within map expressions.                  |
| flattening_enabled  | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth| False    | None    | The max depth to flatten schemas.                                              |

## API Coverage

| API Endpoint                  | Supported | Notes |
| :---------------------------- | :-------: | :---- |
| `/v1/alert-channels`          |    ✅     |       |
| `/v1/alert-notifications`     |    ✅     |       |
| `/v1/checks`                  |    ✅     |       |
| `/v1/check-alerts`            |    ✅     |       |
| `/v1/check-groups`            |    N/A    |       |
| `/v1/check-results/{checkId}` |    N/A    |       |
| `/v1/dashboards`              |    ✅     |       |
| `/v1/locations`               |    ✅     |       |
| `/v1/maintenance-windows`     |    N/A    |       |
| `/v1/private-locations`       |    N/A    |       |
| `/v1/runtimes`                |    ✅     |       |
| `/v1/snippets`                |    ✅     |       |
| `/v1/variables`               |    ✅     |       |

A full list of supported settings and capabilities is available by running: `tap-checkly --about`

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your tap requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `tap-checkly` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-checkly --version
tap-checkly --help
tap-checkly --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and then run:

```bash
poetry run pytest
```

You can also test the `tap-checkly` CLI interface directly using `poetry run`:

```bash
poetry run tap-checkly --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-checkly
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-checkly --version
# OR run a test `elt` pipeline:
meltano elt tap-checkly target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
