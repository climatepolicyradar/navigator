from pathlib import Path
from unittest.mock import patch, MagicMock

from requests import Response

from app.users_add.main import main

TEST_USERS_CSV_1 = str(
    (
        Path(__file__).parent / ".." / ".." / "data" / "test" / "users_test_data.csv"
    ).absolute()
)


@patch("app.users_add.main.post_user")
@patch("app.users_add.main.get_admin_token")
def test_post_users_to_backend_api(mock_get_admin_token, mock_post_user):
    mock_get_admin_token.return_value = "a-super-secret-token"
    mock_post_user.return_value = MagicMock(spec=Response, status_code=200)

    main(TEST_USERS_CSV_1)

    assert mock_get_admin_token.called_once()
    assert mock_post_user.call_count == 2

    # Check names
    assert mock_post_user.call_args_list[0].kwargs["payload"]["names"] == "Paul Chuckle"
    assert (
        mock_post_user.call_args_list[1].kwargs["payload"]["names"] == "Barry Chuckle"
    )

    # Check emails (convert list to str)
    assert (
        mock_post_user.call_args_list[0].kwargs["payload"]["email"]
        == "paul@chuckle.bros"
    )
    assert (
        mock_post_user.call_args_list[1].kwargs["payload"]["email"]
        == "barry@chuckle.bros"
    )

    # Check affiliation type (convert str to list)
    assert mock_post_user.call_args_list[0].kwargs["payload"]["affiliation_type"] == [
        "Comedy"
    ]
    assert mock_post_user.call_args_list[1].kwargs["payload"]["affiliation_type"] == [
        "Drama"
    ]
