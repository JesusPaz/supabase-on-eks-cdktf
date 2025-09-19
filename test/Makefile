# Supabase API Tests Makefile
# Simple commands to setup and run API tests

.PHONY: help install test clean

# Default target
help:
	@echo "🚀 Supabase API Tests"
	@echo ""
	@echo "Available commands:"
	@echo "  make install  - Install Python dependencies"
	@echo "  make test     - Run all API tests"
	@echo "  make clean    - Clean up virtual environment"
	@echo "  make all      - Install + Test (recommended)"
	@echo ""

# Install Python dependencies in virtual environment
install:
	@echo "📦 Setting up virtual environment..."
	python3 -m venv venv
	@echo "📦 Installing dependencies..."
	./venv/bin/pip install -r requirements.txt
	@echo "✅ Dependencies installed in virtual environment"

# Run API tests
test:
	@echo "🧪 Running Supabase API tests..."
	@if [ -d "venv" ]; then \
		./venv/bin/python test_api.py; \
	else \
		echo "⚠️  Virtual environment not found. Run 'make install' first."; \
		python3 test_api.py; \
	fi

# Clean up virtual environment
clean:
	@echo "🧹 Cleaning up virtual environment..."
	rm -rf venv
	@echo "✅ Virtual environment removed"

# Install and test (recommended workflow)
all: install test
	@echo ""
	@echo "🎉 All done! Check the test results above."
	@echo "📊 Expected: 13-14/14 tests should pass"
	@echo "🌐 Dashboard: https://supabase.stack-ai.jesuspaz.com/"
