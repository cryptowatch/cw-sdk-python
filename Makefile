test:
	pytest -vv --ignore tests/test_api.py

test-http-real:
	pytest -vv tests/test_api.py

lint:
	black --check cryptowatch/**/*[^pb2].py tests examples

proto:
	protoc --proto_path=../proto --python_out=cryptowatch/stream/proto ../proto/public/**/*.proto
	sed -i'.original' 's/from public\./from cryptowatch.stream.proto.public./g' cryptowatch/stream/proto/public/**/*_pb2.py

.PHONY: proto lint test
