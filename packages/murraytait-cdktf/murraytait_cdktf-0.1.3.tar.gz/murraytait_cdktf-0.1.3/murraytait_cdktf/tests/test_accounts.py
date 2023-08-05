import json
from mock import patch

from murraytait_cdktf.accounts import Accounts


def read_json_file(filename):
    return json.loads(open(filename, "r").read())


@patch('murraytait_cdktf.accounts.boto3')
def test_service_accounts_info(mock_boto3):
    # Arrange
    session = mock_boto3.Session.return_value
    client = session.client.return_value
    client.list_accounts.return_value = read_json_file(
        "murraytait_cdktf/tests/list_accounts_response.json")

    client.list_tags_for_resource.side_effect = [
        json.loads(
            '{ "Tags":[{"Key": "dns", "Value": "dns"}, {"Key": "build", "Value": "build"}, {"Key": "terraform_state", "Value": "build"}]}'),
        json.loads('{ "Tags":[]}'),
        json.loads('{ "Tags":[]}')
    ]

    # Act
    accounts = Accounts("endtoend", "453254632971_ListAccountsAccess")

    # Assert
    assert accounts is not None
    assert accounts.aws_account_id == "123456789012"
    assert accounts.build_account_id == "210987654321"
    assert accounts.build_account_name == "build"
    assert accounts.dns_account_id == "567890123456"
    assert accounts.terraform_state_account_id == "210987654321"
    assert accounts.terraform_state_account_name == "build"
    assert accounts.build_children_account_ids is None
    assert accounts.terraform_state_children_account_ids is None
    assert accounts.dns_children_account_ids is None


@patch('murraytait_cdktf.accounts.boto3')
def test_build_accounts_info(mock_boto3):
    # Arrange
    session = mock_boto3.Session.return_value
    client = session.client.return_value
    client.list_accounts.return_value = read_json_file(
        "murraytait_cdktf/tests/list_accounts_response.json")

    client.list_tags_for_resource.side_effect = [
        json.loads(
            '{ "Tags":[{"Key": "dns", "Value": "dns"}, {"Key": "build", "Value": "build"}, {"Key": "terraform_state", "Value": "build"}]}'),
        json.loads(
            '{ "Tags":[{"Key": "build", "Value": "build"}, {"Key": "terraform_state", "Value": "build"}]}'),
        json.loads('{ "Tags":[{"Key": "build", "Value": "build"}]}')
    ]

    # Act
    accounts = Accounts("build", "453254632971_ListAccountsAccess")

    # Assert
    assert accounts is not None
    assert accounts.aws_account_id == "210987654321"
    assert accounts.build_account_id == "210987654321"
    assert accounts.build_account_name == "build"
    assert accounts.dns_account_id is None
    assert accounts.terraform_state_account_id == "210987654321"
    assert accounts.terraform_state_account_name == "build"
    assert accounts.build_children_account_ids == [
        "123456789012", "210987654321", "567890123456"]
    assert accounts.terraform_state_children_account_ids == [
        "123456789012", "210987654321"]
    assert accounts.dns_children_account_ids is None


@patch('murraytait_cdktf.accounts.boto3')
def test_dns_accounts_info(mock_boto3):
    # Arrange
    session = mock_boto3.Session.return_value
    client = session.client.return_value
    client.list_accounts.return_value = read_json_file(
        "murraytait_cdktf/tests/list_accounts_response.json")

    client.list_tags_for_resource.side_effect = [
        json.loads(
            '{ "Tags":[{"Key": "dns", "Value": "dns"}, {"Key": "build", "Value": "build"}, {"Key": "terraform_state", "Value": "build"}]}'),
        json.loads(
            '{ "Tags":[{"Key": "build", "Value": "build"}, {"Key": "terraform_state", "Value": "build"}]}'),
        json.loads(
            '{ "Tags":[{"Key": "build", "Value": "build"}, {"Key": "terraform_state", "Value": "build"}]}')
    ]

    # Act
    accounts = Accounts("dns", "453254632971_ListAccountsAccess")

    # Assert
    assert accounts is not None
    assert accounts.aws_account_id == "567890123456"
    assert accounts.build_account_id == "210987654321"
    assert accounts.build_account_name == "build"
    assert accounts.dns_account_id is None
    assert accounts.terraform_state_account_id == "210987654321"
    assert accounts.terraform_state_account_name == "build"
    assert accounts.build_children_account_ids is None
    assert accounts.terraform_state_children_account_ids is None
    assert accounts.dns_children_account_ids == ["123456789012"]
