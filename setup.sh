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
        print_success "Virtual environment '$VENV_DIR' already exists"
        return 0
    else
        print_info "Virtual environment '$VENV_DIR' not found"
        return 1
    fi
}

# Function to check for required tools
check_required_tools() {
    local missing_tools=()
    
    if ! command -v pip3 >/dev/null 2>&1 && ! command -v pip >/dev/null 2>&1; then
        missing_tools+=("pip")
    fi
    
    if ! command -v git >/dev/null 2>&1; then
        missing_tools+=("git")
    fi
    
    if [[ ${#missing_tools[@]} -gt 0 ]]; then
        local tools_list=$(IFS=", " ; echo "${missing_tools[*]}")
        if [[ "$1" == "dry_run" ]]; then
            print_warning "Missing required tools: $tools_list"
        else
            print_error "Missing required tools: $tools_list"
            print_error "Please install the missing tools and run the setup script again."
            exit 1
        fi
        return 1
    else
        print_success "All required tools found (pip, git)"
        return 0
    fi
}

# Function to install dependencies
install_dependencies() {
    if [[ "$1" == "dry_run" ]]; then
        print_dry_run "Would install dependencies from requirements.txt"
        return 0
    fi
    
    print_info "Installing dependencies from requirements.txt..."
    if [[ -d "$VENV_DIR" ]]; then
        source "$VENV_DIR/bin/activate"
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "Virtual environment not found. Please create it first."
        return 1
    fi
}

# Function to install NLTK data
install_nltk_data() {
    if [[ "$1" == "dry_run" ]]; then
        print_dry_run "Would install NLTK data using scripts/install_nltk_data.py"
        return 0
    fi
    
    print_info "Installing NLTK data..."
    if [[ -d "$VENV_DIR" ]]; then
        source "$VENV_DIR/bin/activate"
        python3 scripts/install_nltk_data.py
        print_success "NLTK data installed successfully"
    else
        print_error "Virtual environment not found. Please create it first."
        return 1
    fi
}

# Function to prompt for API keys
prompt_for_api_keys() {
    local pexels_key=""
    local thesaurus_key=""
    
    if [[ "$1" == "dry_run" ]]; then
        print_dry_run "Would prompt for PEXELS_API_KEY"
        print_dry_run "Would prompt for BIG_HUGE_API_KEY"
        return 0
    fi
    
    echo
    print_info "API Keys Configuration"
    echo "You'll need API keys for image search and word associations."
    echo
    
    # Pexels API Key
    while [[ -z "$pexels_key" ]]; do
        read -p "Enter your Pexels API key (or press Enter to skip): " pexels_key
        if [[ -z "$pexels_key" ]]; then
            print_warning "Pexels API key skipped. Image search will not be available."
            pexels_key="your_pexels_api_key"
            break
        fi
    done
    
    # Big Huge Thesaurus API Key
    while [[ -z "$thesaurus_key" ]]; do
        read -p "Enter your Big Huge Thesaurus API key (or press Enter to skip): " thesaurus_key
        if [[ -z "$thesaurus_key" ]]; then
            print_warning "Big Huge Thesaurus API key skipped. Word associations will not be available."
            thesaurus_key="your_big_huge_thesaurus_key"
            break
        fi
    done
    
    # Store keys for .env file creation
    PEXELS_API_KEY="$pexels_key"
    BIG_HUGE_API_KEY="$thesaurus_key"
}

# Function to create .env file
create_env_file() {
    if [[ "$1" == "dry_run" ]]; then
        print_dry_run "Would create .env file with API keys and configuration"
        return 0
    fi
    
    if [[ -f ".env" ]]; then
        print_warning ".env file already exists. Backing up to .env.backup"
        cp .env .env.backup
    fi
    
    print_info "Creating .env file..."
    cat > .env << EOF
# AnkiCardsToolkit Environment Configuration
# This file contains API keys and configuration settings

# Anki Configuration
MODEL_NAME=VocabCard_English_UA
DECK_NAME=Default
ANKI_CONNECT_URL=http://localhost:8765
CONFIG_FILE=last_deck.txt

# API Keys
PEXELS_API_KEY=$PEXELS_API_KEY
BIG_HUGE_API_KEY=$BIG_HUGE_API_KEY

# TTS Configuration
TTS_PROVIDER=gtts

# User Interface
USER_LOCALE=uk
EOF
    
    print_success ".env file created successfully"
}

# Function to show what would be done in dry run
show_dry_run_plan() {
    print_dry_run "Would perform the following actions:"
    
    if ! check_python_version >/dev/null 2>&1; then
        print_dry_run "  - Install Python 3.11 or higher"
    fi
    
    if ! check_venv >/dev/null 2>&1; then
        print_dry_run "  - Create virtual environment '$VENV_DIR'"
        print_dry_run "  - Activate virtual environment"
        print_dry_run "  - Install dependencies from requirements.txt"
    else
        print_dry_run "  - Activate existing virtual environment"
        print_dry_run "  - Install/update dependencies from requirements.txt"
    fi
    
    print_dry_run "  - Install NLTK data"
    print_dry_run "  - Prompt for API keys (Pexels, Big Huge Thesaurus)"
    print_dry_run "  - Create .env file with configuration"
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
    
    # Check required tools
    print_info "Checking required tools..."
    if [[ "$dry_run" == true ]]; then
        check_required_tools "dry_run"
    else
        check_required_tools
    fi
    echo
    
    # Install dependencies
    print_info "Installing dependencies..."
    if [[ "$dry_run" == true ]]; then
        install_dependencies "dry_run"
    else
        install_dependencies
    fi
    echo
    
    # Install NLTK data
    print_info "Installing NLTK data..."
    if [[ "$dry_run" == true ]]; then
        install_nltk_data "dry_run"
    else
        install_nltk_data
    fi
    echo
    
    # Prompt for API keys
    if [[ "$dry_run" == true ]]; then
        prompt_for_api_keys "dry_run"
    else
        prompt_for_api_keys
    fi
    echo
    
    # Create .env file
    print_info "Creating configuration file..."
    if [[ "$dry_run" == true ]]; then
        create_env_file "dry_run"
    else
        create_env_file
    fi
    echo
    
    if [[ "$dry_run" == true ]]; then
        show_dry_run_plan
        echo
        print_info "Dry run completed. No changes were made to the system."
    else
        print_success "Setup completed successfully!"
        print_info "You can now run: python3 generate_card.py"
    fi
}

# Run main function with all arguments
main "$@" 