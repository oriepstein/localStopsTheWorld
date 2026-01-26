
name: Validate Sight IDs

on:
  push:
    paths:
      - "**/*.json"
  pull_request:
    paths:
      - "**/*.json"

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Validate and add IDs
        run: |
          for file in $(git diff --name-only ${{ github.event.before }} ${{ github.sha }} | grep '\.json$'); do
            echo "Processing $file"
            python scripts/add_ids_to_sights.py "$file"
          done
