import atexit
import os
import subprocess
import sys

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
    KiwoomOpenApiPlusQAxWidgetMixin,
)
from koapy.utils.ctypes import is_admin
from koapy.utils.logging.Logging import Logging
from koapy.utils.platform import is_32bit
from koapy.utils.subprocess import function_to_subprocess_args


class KiwoomOpenApiPlusVersionUpdater(Logging):
    def __init__(self, credentials):
        self._credentials = credentials

    def disable_autologin(self):
        self.logger.info("Disabling auto login")
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTypeLib import (
            API_MODULE_PATH,
        )

        module_path = API_MODULE_PATH
        autologin_dat = os.path.join(module_path, "system", "Autologin.dat")
        if os.path.exists(autologin_dat):
            self.logger.info("Removing %s", autologin_dat)
            os.remove(autologin_dat)
            self.logger.info("Disabled auto login")
            return True
        else:
            self.logger.info("Autologin is already disabled")
            return False

    @classmethod
    def open_login_window_impl(cls):
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
            KiwoomOpenApiPlusError,
        )
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
            KiwoomOpenApiPlusQAxWidget,
        )
        from koapy.compat.pyside2.QtWidgets import QApplication

        cls.logger.info("Opening login window")
        app = QApplication(sys.argv)
        control = KiwoomOpenApiPlusQAxWidget()
        if control.GetConnectState() == 0:

            def OnEventConnect(errcode):
                control.OnEventConnect.disconnect(OnEventConnect)
                KiwoomOpenApiPlusError.try_or_raise(errcode)
                app.exit(errcode)

            control.OnEventConnect.connect(OnEventConnect)
            KiwoomOpenApiPlusError.try_or_raise(control.CommConnect())
        return app.exec_()

    def open_login_window(self):
        # opening login window is a blocking process. (`app.exec_()` is the blocking process and will wait for `app.exit()`)
        # also it's hard to use both PySide2/PyQt5 and pywinauto at the same time in the same process due to compatibility issue.
        #
        # in order to avoid the issues mentioned above we are creating login window in a separate process.
        # and then will do login using pywinauto in another process using `__login_using_pywinauto()` function.
        #
        # this process will stay live until `OnEventConnect` event happens, hopefully a successful login.
        #
        # for more information about the compatibility issue between PySide2/PyQt5 and pywinauto, check the following link:
        #   https://github.com/pywinauto/pywinauto/issues/472

        def main():
            # pylint: disable=redefined-outer-name,import-self
            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
                KiwoomOpenApiPlusVersionUpdater,
            )

            KiwoomOpenApiPlusVersionUpdater.open_login_window_impl()

        cmd = function_to_subprocess_args(main)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = subprocess.Popen(cmd, creationflags=creationflags)
        atexit.register(proc.kill)
        return proc

    @classmethod
    def show_account_window_impl(cls):
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
            KiwoomOpenApiPlusError,
        )
        from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget import (
            KiwoomOpenApiPlusQAxWidget,
        )
        from koapy.compat.pyside2.QtWidgets import QApplication

        cls.logger.info("Showing account window")
        app = QApplication(sys.argv)
        control = KiwoomOpenApiPlusQAxWidget()
        if control.GetConnectState() == 0:

            def OnEventConnect(errcode):
                control.OnEventConnect.disconnect(OnEventConnect)
                KiwoomOpenApiPlusError.try_or_raise(errcode)
                control.KOA_Functions("ShowAccountWindow", "")
                app.exit(errcode)

            control.OnEventConnect.connect(OnEventConnect)
            KiwoomOpenApiPlusError.try_or_raise(control.CommConnect())
        return app.exec_()

    def show_account_window(self):
        # this function does pretty much the same job like the `__open_login_window()` function.
        # but the difference is that it will show up the account setting window after successful login,
        # so that we can (re-)enable the auto login functionality provided by the OpenAPI itself.
        #
        # this process will stay live until the account window is closed in the `OnEventConnect` event,
        # hopefully after successfully enabling the auto login functionality.
        #
        # note that the `control.KOA_Functions('ShowAccountWindow', '')` line is also blocking process.
        # so it will block until the account window is closed after enabling the auto login.

        def main():
            # pylint: disable=redefined-outer-name,import-self
            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater import (
                KiwoomOpenApiPlusVersionUpdater,
            )

            KiwoomOpenApiPlusVersionUpdater.show_account_window_impl()

        cmd = function_to_subprocess_args(main)
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP
        proc = subprocess.Popen(cmd, creationflags=creationflags)
        atexit.register(proc.kill)
        return proc

    @classmethod
    def enable_autologin_using_pywinauto(cls, account_passwords):
        import pywinauto

        is_in_development = False

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        account_window = desktop.window(title_re=r"계좌비밀번호 입력 \(버전: [0-9]+.+[0-9]+\)")

        try:
            cls.logger.info("Waiting for account window to show up")
            timeout_account_window_ready = 15
            account_window.wait("ready", timeout_account_window_ready)
        except pywinauto.timings.TimeoutError:
            cls.logger.info("Cannot find account window")
            raise
        else:
            cls.logger.info("Account window found")
            if is_in_development:
                account_window.logging.info_control_identifiers()

            cls.logger.info("Enabling auto login")
            account_window["CheckBox"].check()

            account_combo = account_window["ComboBox"]
            account_cnt = account_combo.item_count()

            cls.logger.info("Putting account passwords")
            for i in range(account_cnt):
                account_combo.select(i)
                account_no = account_combo.selected_text().split()[0]
                if account_no in account_passwords:
                    account_window["Edit"].set_text(account_passwords[account_no])
                elif "0000000000" in account_passwords:
                    account_window["Edit"].set_text(account_passwords["0000000000"])
                account_window["등록"].click()

            cls.logger.info("Closing account window")
            account_window["닫기"].click()

            try:
                cls.logger.info("Waiting account window to be closed")
                timeout_account_window_done = 5
                account_window.wait_not("visible", timeout_account_window_done)
            except pywinauto.timings.TimeoutError as e:
                cls.logger.info("Cannot sure account window is closed")
                raise RuntimeError("Cannot sure account window is closed") from e
            else:
                cls.logger.info("Account window closed")

    @classmethod
    def check_apply_simulation_window(cls):
        import pywinauto

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        apply_simulation_window = desktop.window(title="모의투자 참가신청")

        try:
            timeout_apply_simulation = 10
            apply_simulation_window.wait("ready", timeout_apply_simulation)
        except pywinauto.timings.TimeoutError:
            pass
        else:
            cls.logger.warning("Please apply for simulation server before using it")
            raise RuntimeError("Please apply for simulation server before using it")

    @classmethod
    def login_using_pywinauto(cls, credentials):
        # reusing the implementation in the mixin
        KiwoomOpenApiPlusQAxWidgetMixin.LoginUsingPywinauto_Impl(credentials)
        cls.check_apply_simulation_window()

    def enable_autologin(self):
        self.logger.info("Start enabling auto login")

        # pylint: disable=unused-variable
        account_window_proc = self.show_account_window()

        credentials = self._credentials
        account_passwords = credentials.get("account_passwords")

        self.login_using_pywinauto(credentials)
        self.enable_autologin_using_pywinauto(account_passwords)

    def try_version_update_using_pywinauto(self):
        import pywinauto

        self.logger.info("Trying version update")
        self.disable_autologin()

        login_window_proc = self.open_login_window()

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        login_window = desktop.window(title="Open API Login")

        credentials = self._credentials
        self.login_using_pywinauto(credentials)

        timeout_login_successful = 4
        timeout_version_check = 1
        timeout_per_trial = timeout_login_successful + timeout_version_check

        trial_timeout = 180
        trial_count = trial_timeout / timeout_per_trial
        while trial_count > 0:
            try:
                self.logger.info(
                    "Login in progress ... timeout after %d sec",
                    trial_count * timeout_per_trial,
                )
                trial_count -= 1
                login_window.wait_not("exists", timeout_login_successful)
                if login_window.exists():
                    # make sure that login_window control does not exist.
                    continue
            except pywinauto.timings.TimeoutError as e:
                version_window = desktop.window(title="opstarter")
                try:
                    version_window.wait("ready", timeout_version_check)
                except pywinauto.timings.TimeoutError:
                    continue
                else:
                    self.logger.info("Version update required")

                    self.logger.info("Closing login app")
                    login_window_proc.kill()
                    login_window_proc.wait()
                    self.logger.info("Killed login app process")
                    timeout_login_screen_closed = 30
                    login_window.close(timeout_login_screen_closed)
                    try:
                        login_window.wait_not("visible", timeout_login_screen_closed)
                    except pywinauto.timings.TimeoutError as e:
                        self.logger.info("Cannot close login window")
                        raise RuntimeError("Cannot close login window") from e
                    else:
                        self.logger.info("Closed login window")

                        self.logger.info("Starting to update version")
                        version_window["Button"].click()

                        versionup_window = desktop.window(title="opversionup")
                        confirm_window = desktop.window(title="업그레이드 확인")

                        try:
                            self.logger.info("Waiting for possible failure")
                            timeout_confirm_update = 10
                            versionup_window.wait("ready", timeout_confirm_update)
                        except pywinauto.timings.TimeoutError:
                            self.logger.info("Cannot find failure confirmation popup")
                        else:
                            self.logger.info("Failed to update")
                            raise RuntimeError("Failed to update") from e

                        try:
                            self.logger.info(
                                "Waiting for confirmation popup after update"
                            )
                            timeout_confirm_update = 10
                            confirm_window.wait("ready", timeout_confirm_update)
                        except pywinauto.timings.TimeoutError as e:
                            self.logger.info("Cannot find confirmation popup")
                            raise RuntimeError("Cannot find confirmation popup") from e
                        else:
                            self.logger.info("Confirming update")
                            confirm_window["Button"].click()

                        self.logger.info("Done update")
                        self.logger.info("Enabling auto login back")
                        self.enable_autologin()
                        self.logger.info("Done update, enabled auto login")

                        return True
            else:
                self.logger.info("Login ended successfully")
                self.logger.info("No version update required")
                self.logger.info("Enabling auto login back")
                self.enable_autologin()
                self.logger.info("There was no version update, enabled auto login")
                return False
        return False

    def update_version_if_necessary(self):
        assert (
            is_32bit()
        ), "Automatic version update requires to be run in 32bit environment"
        assert (
            is_admin()
        ), "Automatic version update requires to be run as administrator"
        return self.try_version_update_using_pywinauto()
