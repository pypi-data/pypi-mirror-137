import pytest

from viresclient._client import ClientRequest
from viresclient import SwarmRequest, AeolusRequest
import viresclient


def test_ClientRequest():
    """Test that a ClientRequest gets set up correctly.
    """
    request = ClientRequest('dummy_url')
    assert isinstance(request._wps_service,
                      viresclient._wps.wps_vires.ViresWPS10Service
                      )
    request = SwarmRequest('dummy_url')
    assert isinstance(request._wps_service,
                      viresclient._wps.wps_vires.ViresWPS10Service
                      )
    request = AeolusRequest('dummy_url')
    assert isinstance(request._wps_service,
                      viresclient._wps.wps_vires.ViresWPS10Service
                      )


def test_SwarmRequest():
    """Basic test that the SwarmRequest can be created
    
    Requires configured token to be available to to the test environment
    """
    request = SwarmRequest("https://vires.services/ows")
    assert request._server_type == "Swarm"
    request.list_jobs()


def test_AeolusRequest():
    """Basic test that the AeolusRequest can be created
    
    Requires configured token to be available to to the test environment
    """
    request = AeolusRequest("https://aeolus.services/ows")
    assert request._server_type == "Aeolus"
    request.list_jobs()