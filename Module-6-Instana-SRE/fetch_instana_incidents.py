#!/usr/bin/env python3
"""
Instana Incident Fetcher

This script connects to the Instana API and fetches the latest 5 open incidents.
The incident data is saved to a JSON file for further analysis.

Requirements:
    - python-dotenv: For loading environment variables
    - requests: For making HTTP API calls
    
Install dependencies:
    pip install python-dotenv requests
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InstanaAPIClient:
    """Client for interacting with the Instana API."""
    
    def __init__(self, host: str, api_key: str):
        """
        Initialize the Instana API client.
        
        Args:
            host: The Instana host URL (e.g., https://example.instana.io)
            api_key: The API key for authentication
        """
        # Clean up the host URL - remove any hash fragments and trailing slashes
        self.base_url = host.split('#')[0].rstrip('/')
        
        # Construct the API base URL
        # Instana API typically uses /api/events/issues endpoint for incidents
        if '/api' not in self.base_url:
            self.api_base_url = f"{self.base_url}/api"
        else:
            self.api_base_url = self.base_url
            
        self.api_key = api_key
        self.headers = {
            'Authorization': f'apiToken {api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info(f"Initialized Instana API client for host: {self.base_url}")
    
    def fetch_open_incidents(self, limit: int = 5) -> Optional[List[Dict]]:
        """
        Fetch open incidents from Instana.
        
        The Instana API uses the /api/events/issues endpoint to retrieve incidents.
        We filter for open incidents and limit the results.
        
        Args:
            limit: Maximum number of incidents to fetch (default: 5)
            
        Returns:
            List of incident dictionaries, or None if the request fails
        """
        # Instana API endpoint for events/incidents
        # The correct endpoint is /api/events (not /api/events/issues)
        endpoint = f"{self.api_base_url}/events"
        
        # Query parameters to filter for open incidents
        # windowSize is in milliseconds (24 hours = 86400000 ms)
        # to is the end time (current time in milliseconds)
        # from is calculated as to - windowSize
        current_time_ms = int(datetime.now().timestamp() * 1000)
        params = {
            'to': current_time_ms,
            'windowSize': 86400000,  # Look back 24 hours
            'eventTypeFilters': 'incident',  # Filter for incidents only
            'size': limit  # Limit the number of results
        }
        
        try:
            logger.info(f"Fetching open incidents from: {endpoint}")
            logger.debug(f"Request parameters: {params}")
            
            response = requests.get(
                endpoint,
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            # Log response status
            logger.info(f"API Response Status: {response.status_code}")
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse JSON response
            data = response.json()
            
            # Instana API returns incidents in the 'items' field for /api/events endpoint
            # or directly as a list
            if isinstance(data, list):
                incidents = data
            else:
                incidents = data.get('items', data.get('issues', []))
            
            logger.info(f"Successfully fetched {len(incidents)} open incidents")
            return incidents
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching incidents from Instana API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response content: {e.response.text}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None


def save_incidents_to_file(incidents: List[Dict], filename: str = 'incidents.json') -> bool:
    """
    Save incident data to a JSON file.
    
    Args:
        incidents: List of incident dictionaries
        filename: Output filename (default: incidents.json)
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Add metadata to the output
        output_data = {
            'metadata': {
                'fetch_timestamp': datetime.utcnow().isoformat() + 'Z',
                'incident_count': len(incidents),
                'status': 'OPEN'
            },
            'incidents': incidents
        }
        
        # Write to file with pretty formatting
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Successfully saved {len(incidents)} incidents to {filename}")
        return True
        
    except IOError as e:
        logger.error(f"Error writing to file {filename}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error saving incidents: {e}")
        return False


def main():
    """Main function to fetch and save Instana incidents."""
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Get configuration from environment variables
    instana_host = os.getenv('INSTANA_HOST')
    instana_api_key = os.getenv('INSTANA_API_KEY')
    
    # Validate configuration
    if not instana_host:
        logger.error("INSTANA_HOST not found in environment variables")
        return False
    
    if not instana_api_key:
        logger.error("INSTANA_API_KEY not found in environment variables")
        return False
    
    logger.info("Starting Instana incident fetch process")
    
    # Initialize API client
    client = InstanaAPIClient(instana_host, instana_api_key)
    
    # Fetch open incidents
    incidents = client.fetch_open_incidents(limit=5)
    
    if incidents is None:
        logger.error("Failed to fetch incidents")
        return False
    
    if len(incidents) == 0:
        logger.warning("No open incidents found")
        # Still save an empty result
        save_incidents_to_file(incidents)
        return True
    
    # Save incidents to file
    success = save_incidents_to_file(incidents)
    
    if success:
        logger.info("Incident fetch process completed successfully")
        return True
    else:
        logger.error("Failed to save incidents to file")
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)

# Made with Bob
