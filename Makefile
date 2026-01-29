.PHONY: setup lint test-unit test-integration test cdk-synth verify verify-aws demo-aws-planner smoke-aws-planner

setup:
	python3 -m pip install pydantic boto3 pytest ruff
	cd infra/cdk && npm install

lint:
	ruff check services tests

test-unit:
	pytest tests/unit

test-integration:
	pytest tests/integration

test: test-unit test-integration

demo-local:
	python3 scripts/demo_local.py

demo-local-planner:
	python3 scripts/demo_local_planner.py

demo-local-bedrock:
	python3 scripts/demo_local_bedrock_planner.py

cdk-install:
	npm --prefix infra/cdk install

cdk-synth:
	cd infra/cdk && npx cdk synth

cdk-deploy:
	cd infra/cdk && npx cdk deploy --require-approval never

smoke-aws:
	python3 scripts/smoke_aws.py

demo-aws:
	python3 scripts/demo_aws.py

demo-aws-planner:
	python3 scripts/demo_aws_planner.py

smoke-aws-planner:
	python3 scripts/smoke_aws_planner.py

verify: lint test demo-local

verify-aws:
	@if [ -z "$$AWS_PROFILE" ]; then \
		echo "AWS_PROFILE is not set. Run: AWS_PROFILE=<profile> make verify-aws"; \
		exit 1; \
	fi
	$(MAKE) cdk-synth
	$(MAKE) cdk-deploy
	$(MAKE) smoke-aws
	$(MAKE) demo-aws
	$(MAKE) smoke-aws-planner
	$(MAKE) demo-aws-planner
