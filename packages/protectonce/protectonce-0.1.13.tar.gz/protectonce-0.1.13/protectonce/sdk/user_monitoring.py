from ..core_interface import invoke_core_method
from ..rules.handlers import cls
from .. import common_utils
from ..instrument.po_exceptions import SecurityException


def __get_session_id():
    data = {
        "config": {
            "property": "__poSessionId"
        }
    }

    return cls.get_property(data)


def report_signup(user_name):
    """input parameters user_name as string"""
    if not isinstance(user_name, str):
        print(
            "[PROTECTONCE_ERROR] protectonce.report_signup: 'user_name' should be string")
        return
    blocked = False
    try:
        po_session_id = __get_session_id()
        signup_data = {"data": {
            "poSessionId": po_session_id,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.storeSignUpData", signup_data)
        blocked = common_utils.is_action_blocked(result)
        print(f'Result_actions=={result}')
    except:
        print(
            "[PROTECTONCE_ERROR] protectonce.report_signup: Error occured while handling signup data")

    if blocked:
        raise SecurityException(f'{user_name} user is blocked')


def report_login(status, user_name):
    """input parameters status as boolean 'True' or 'False' and user_name as string"""

    if not isinstance(user_name, str) or not isinstance(status, bool):
        print(
            "[PROTECTONCE_ERROR] protectonce.report_login: 'user_name' and 'status' should be boolean either 'True' or 'False'")
        return

    blocked = False
    try:
        po_session_id = __get_session_id()
        login_data = {"data": {
            "poSessionId": po_session_id,
            "success": status,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.storeLoginData", login_data)
    except:
        print(
            "[PROTECTONCE_ERROR] protectonce.report_login: Error occured while handling login data")
    blocked = common_utils.is_action_blocked(result)
    if blocked:
        raise SecurityException(f'{user_name} user is blocked')


def report_auth(user_name, traits=None):
    """input parameters user_name as string traits is optional"""
    if not isinstance(user_name, str):
        print(
            "[PROTECTONCE_ERROR] protectonce.report_auth: 'user_name' should be string")
        return
    blocked = False
    try:
        po_session_id = __get_session_id()
        auth_data = {"data": {
            "poSessionId": po_session_id,
            "userName": user_name
        }}
        result, out_data_type, out_data_size = invoke_core_method(
            "userMonitoring.identify", auth_data)

        blocked = common_utils.is_action_blocked(result)
    except:
        print(
            "[PROTECTONCE_ERROR] protectonce.report_auth: Error occured while handling authentication data")
    if blocked:
        raise SecurityException(f'{user_name} user is blocked')
