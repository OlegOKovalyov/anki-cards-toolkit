#!/bin/bash

# AnkiCardsToolkit Setup Script
# POSIX-compliant setup script for Linux/macOS

set -euo pipefail

VENV_DIR="venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_dry_run() {
    echo -e "${YELLOW}[DRY RUN] $1${NC}"
}

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v lsb_release >/dev/null 2>&1; then
            OS_NAME=$(lsb_release -si)
            OS_VERSION=$(lsb_release -sr)
        elif [[ -f /etc/os-release ]]; then
            OS_NAME=$(grep '^NAME=' /etc/os-release | cut -d'"' -f2)
            OS_VERSION=$(grep '^VERSION=' /etc/os-release | cut -d'"' -f2)
        else
            OS_NAME="Linux"
            OS_VERSION="Unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS_NAME="macOS"
        OS_VERSION=$(sw_vers -productVersion)
    else
        OS_NAME="Unknown"
        OS_VERSION="Unknown"
    fi
}

# Function to check Python version
check_python_version() {
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
        PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)
        
        if [[ "$PYTHON_MAJOR" -eq 3 && "$PYTHON_MINOR" -ge 11 ]]; then
            print_success "Python $PYTHON_VERSION found (meets requirement: 3.11+)"
            return 0
        else
            print_warning "Python $PYTHON_VERSION found (requires 3.11+)"
            return 1
        fi
    else
        print_error "Python 3 not found"
        return 1
    fi
}

# Function to check if virtual environment exists
check_venv() {
    if [[ -d "$VENV_DIR" ]]; then
        print_success "Virtual environment 'venv' already exists"
        return 0
    else
        print_info "Virtual environment 'venv' not found"
        return 1
    fi
}

# Function to show what would be done in dry run
show_dry_run_plan() {
    print_dry_run "Would perform the following actions:"
    
    if ! check_python_version >/dev/null 2>&1; then
        print_dry_run "  - Install Python 3.11 or higher"
    fi
    
    if ! check_venv >/dev/null 2>&1; then
        print_dry_run "  - Create virtual environment 'venv'"
        print_dry_run "  - Activate virtual environment"
        print_dry_run "  - Install dependencies from requirements.txt"
    else
        print_dry_run "  - Activate existing virtual environment"
        print_dry_run "  - Install/update dependencies from requirements.txt"
    fi
    
    print_dry_run "  - Generate 1-second silent audio file"
    print_dry_run "  - Install NLTK data"
    print_dry_run "  - Create .env file template"
}

# Main function
main() {
    local dry_run=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry|--dry-run)
                dry_run=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --dry, --dry-run    Show what would be done without making changes"
                echo "  -h, --help          Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use -h or --help for usage information"
                exit 1
                ;;
        esac
    done
    
    print_info "AnkiCardsToolkit Setup Script"
    echo
    
    # Detect OS
    detect_os
    print_info "Operating System: $OS_NAME $OS_VERSION"
    echo
    
    # Check if OS is supported
    if [[ "$OS_NAME" == "Unknown" ]]; then
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    
    if [[ "$OS_NAME" == "macOS" || "$OS_NAME" == *"Ubuntu"* || "$OS_NAME" == *"Debian"* || "$OS_NAME" == *"CentOS"* || "$OS_NAME" == *"Red Hat"* || "$OS_NAME" == *"Fedora"* ]]; then
        print_success "Supported operating system detected"
    else
        print_warning "Operating system may not be fully supported: $OS_NAME"
    fi
    echo
    
    # Check Python version
    print_info "Checking Python installation..."
    check_python_version
    echo
    
    # Check virtual environment
    print_info "Checking virtual environment..."
    check_venv
    echo
    
    if [[ "$dry_run" == true ]]; then
        show_dry_run_plan
        echo
        print_info "Dry run completed. No changes were made to the system."
    else
        print_info "Setup script is ready to proceed with installation."
        print_info "Run with --dry-run to see what would be done."
    fi
}

# Run main function with all arguments
main "$@" 