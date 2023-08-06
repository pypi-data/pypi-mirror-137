# arxiv-qa
arXiv Quality Analysis

## Synchronizing Data to GCS

We have two GCS buckets set up in project `arxiv-production`:
- `arxiv-submission` - for submission data
- `arxiv-submission-qa` - for submission QA (meta)data

Both buckets have versioning enabled:

```bash
$ gsutil versioning set ON gs://arxiv-submission
$ gsutil versioning set ON gs://arxiv-submission-qa
```

The `arxiv-submission` bucket also has Pub/Sub notifications enabled:

```bash
$ gsutil notification create -f json gs://arxiv-submission

Created Cloud Pub/Sub topic projects/arxiv-production/topics/arxiv-submission
Created notification config projects/_/buckets/arxiv-submission/notificationConfigs/2
```

### Submission Data

Simple transfers can be handled with shell scripts that wrap `gsutil`, such as [sync_submission.sh](https://github.com/arXiv/arxiv-bin/blob/683b945d639aa9da7ec14029809f07fcc527f83b/sync_submission.sh) in [arxiv-bin](https://github.com/arXiv/arxiv-bin).
```bash
#!/bin/bash
# 2021-08-25 - synchronize submission data to GCS bucket

PATH=/opt_arxiv/python3.6/bin:$PATH
BOTO_CONFIG="/users/busybody/.boto"
SUBMISSION_ID=$1
DATA_NEW=/data/new/${SUBMISSION_ID:0:4}/${SUBMISSION_ID}
BUCKET=arxiv-submission

re='^[0-9]+$'
if ! [[ ${SUBMISSION_ID} =~ $re ]] ; then
  echo "Error: not a number" >&2; exit 1
fi

if [[ -d ${DATA_NEW} ]] ; then
  echo "${DATA_NEW} exists. Proceeding."
  gsutil -m rsync -c -j bib,bbl,html,json,log,meta,tex,txt -x "removed/.*$" -re $DATA_NEW gs://$BUCKET/$SUBMISSION_ID
else
  echo "${DATA_NEW} not found." >&2; exit 1
fi
```

This is currently called at submission time and upon successful processing of uploaded submission files.

### Submission Metadata

See `metadata/README.md`.

### Report Models (Schema)

pydantic models for the QA reports and summary reports are defined in
`arxiv.qa.report.models`.

The schema for the summary report also includes the definition of an
individual report:

```python
from arxiv.qa.report.models import SummaryReport
print(SummaryReport.schema_json(indent=2))

{
  "title": "SummaryReport",
  "type": "object",
  "properties": {
    "name": {
      "title": "Name",
      "default": "arXiv Submission QA Summary Report",
      "type": "string"
    },
    "key_name": {
      "title": "Key Name",
      "default": "qa-summary",
      "type": "string"
    },
    "version": {
      "title": "Version",
      "default": "1.0",
      "type": "string"
    },
    "submission_id": {
      "title": "Submission Id",
      "type": "integer"
    },
    "created": {
      "title": "Created",
      "type": "string"
    },
    "reports": {
      "title": "Reports",
      "default": [],
      "type": "array",
      "items": {
        "$ref": "#/definitions/Report"
      }
    },
    "flagged_report_keys": {
      "title": "Flagged Report Keys",
      "default": [],
      "type": "array",
      "items": {
        "type": "string"
      }
    }
  },
  "required": [
    "submission_id"
  ],
  "definitions": {
    "Flag": {
      "title": "Flag",
      "type": "object",
      "properties": {
        "id": {
          "title": "Id",
          "type": "string"
        },
        "description": {
          "title": "Description",
          "description": "details on what was flagged",
          "type": "string"
        }
      },
      "required": [
        "id"
      ]
    },
    "Report": {
      "title": "Report",
      "type": "object",
      "properties": {
        "name": {
          "title": "Report Name",
          "description": "The full name of the report",
          "type": "string"
        },
        "key_name": {
          "title": "Report Key Name",
          "description": "The abbreviated name of the report",
          "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$",
          "examples": [
            "arxiv-example-report"
          ],
          "type": "string"
        },
        "version": {
          "title": "Version",
          "type": "string"
        },
        "submission_id": {
          "title": "Submission Id",
          "type": "integer"
        },
        "created": {
          "title": "Created",
          "type": "string"
        },
        "flags": {
          "title": "Flags",
          "default": [],
          "type": "array",
          "items": {
            "$ref": "#/definitions/Flag"
          }
        },
        "qa_exec_time_sec": {
          "title": "Qa Exec Time Sec",
          "description": "Time it took to complete the QA check(s) for this report, in seconds.",
          "minimum": 0,
          "type": "integer"
        },
        "data": {
          "title": "Data",
          "type": "object"
        }
      },
      "required": [
        "name",
        "key_name",
        "version",
        "submission_id",
        "data"
      ]
    }
  }
}
```

Building a report:
```python
from arxiv.qa.report.models import Report, SummaryReport

foo_report = Report(
    name="Foo Report",
    key_name="foo-check",
    submission_id=1234,
    version="1.0",
    data={"bar": "baz"},
)

print(foo_report.json(indent=2))
{
  "name": "Foo Report",
  "key_name": "foo-check",
  "version": "1.0",
  "submission_id": 1234,
  "created": "2022-01-25T14:09:34.317039+00:00",
  "flags": [],
  "qa_exec_time_sec": null,
  "data": {
    "bar": "baz"
  }
}

```
Additional examples available in `arxiv.qa.report.tests.test_report_models.py`.

Working with the DB model:
```python
from arxiv.qa.report.models import SubmissionQAReport
from arxiv.qa.report.tabels import DBSubmissionQAReport
db_qar = DBSubmissionQAReport(id=1, submission_id=1234567, report_key_name='fulltext', num_flags=0, report='{"foo": "bar", "baz": 123}')
db_qar_model = SubmissionQAReport.from_orm(db_qar)
print(db_qar_model.json(indent=2))
{
  "id": 1,
  "submission_id": 1234567,
  "report_key_name": "fulltext",
  "created": null,
  "num_flags": 0,
  "report": {
    "foo": "bar",
    "baz": 123
  },
  "report_uri": null
}

```
### Building the arxiv-qa package
First edit `setup.py` and update the `version` parameter if minting a new version.

```python
$ cd arxiv-qa
$ rm -rf dist
# Verify that the version in setup.py is correct
$ pipenv run python setup.py sdist
$ pipenv run twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: <user>
Enter your password: <pass>
```
