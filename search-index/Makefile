build_opensearch:
	docker-compose up -f docker-compose.opensearch.yml build

run_opensearch:
	docker-compose up -f docker-compose.opensearch.yml up

check_opensearch:
	curl -XGET http://localhost:9200 -u 'admin:admin' --insecure
