import json
import os
import queue
import subprocess

from typing import Any, Callable, Dict, Mapping, Optional, Union, overload

from wrapt import synchronized

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions import (
    KiwoomOpenApiPlusDispatchFunctions,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
)
from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter import (
    KiwoomOpenApiPlusCommRqDataRateLimiter,
    KiwoomOpenApiPlusSendConditionRateLimiter,
    KiwoomOpenApiPlusSendOrderRateLimiter,
)
from koapy.backend.kiwoom_open_api_plus.utils.list_conversion import string_to_list
from koapy.config import config
from koapy.utils.ctypes import is_admin
from koapy.utils.logging.Logging import Logging
from koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor import QRateLimitedExecutor
from koapy.utils.subprocess import function_to_subprocess_args


class KiwoomOpenApiPlusQAxWidgetUniversalMixin(KiwoomOpenApiPlusDispatchFunctions):
    def IsConnected(self):
        return self.GetConnectState() == 1

    def ShowAccountWindow(self):
        return self.KOA_Functions("ShowAccountWindow", "")

    def GetServerGubun(self):
        gubun = self.KOA_Functions("GetServerGubun", "")
        if not gubun:
            gubun = self.GetLoginInfo("GetServerGubun")
        return gubun

    def IsSimulationServer(self):
        gubun = self.GetServerGubun()
        return gubun == "1"

    def IsRealServer(self):
        return not self.IsSimulationServer()

    def GetMasterStockInfo(self, code):
        return self.KOA_Functions("GetMasterStockInfo", code)

    def GetMasterStockInfoAsDict(self, code):
        result = self.GetMasterStockInfo(code)
        items = string_to_list(result, sep=";")
        items = [string_to_list(item, sep="|") for item in items]
        info = dict(items)
        return info

    def SetConditionSearchFlag(self, flag):
        return self.KOA_Functions("SetConditionSearchFlag", flag)

    def AddPriceToConditionSearchResult(self):
        return self.SetConditionSearchFlag("AddPrice")

    def DelPriceFromConditionSearchResult(self):
        return self.SetConditionSearchFlag("DelPrice")

    def GetUpjongCode(self, code):
        """
        두번째 인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
        0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100
        """
        code = str(code)
        return self.KOA_Functions("GetUpjongCode", code)

    def GetUpjongCodeAsList(self, code):
        result = self.GetUpjongCode(code)
        items = string_to_list(result, sep="|")
        items = [string_to_list(item, sep=",") for item in items]
        items = [tuple(item) for item in items]
        return items

    def GetUpjongNameByCode(self, code):
        return self.KOA_Functions("GetUpjongNameByCode", code)

    def IsOrderWarningETF(self, code):
        """
        투자유의 종목인 경우 "1" 값이 리턴, 그렇지 않은 경우 "0" 값 리턴. (ETF가 아닌 종목을 입력시 "0" 값 리턴.)
        """
        return self.KOA_Functions("IsOrderWarningETF", code)

    def IsOrderWarningETFAsBoolean(self, code):
        return_code = self.IsOrderWarningETF(code)
        return_code = int(return_code)
        return_code = bool(return_code)
        return return_code

    def IsOrderWarningStock(self, code):
        """
        리턴 값 - "0":해당없음, "2":정리매매, "3":단기과열, "4":투자위험, "5":투자경고
        """
        return self.KOA_Functions("IsOrderWarningStock", code)

    def IsOrderWarningStockAsBoolean(self, code):
        return_code = self.IsOrderWarningStock(code)
        return_code = int(return_code)
        return_code = bool(return_code)
        return return_code

    def GetMasterListedStockCntEx(self, code):
        return self.KOA_Functions("GetMasterListedStockCntEx", code)

    def GetMasterListedStockCntExAsInt(self, code):
        count = self.GetMasterListedStockCntEx(code)
        count = int(count)
        return count

    def GetCodeListByMarketAsList(self, market: Optional[Union[str, int]] = None):
        if market is None:
            market = ""
        market = str(market)
        result = self.GetCodeListByMarket(market)
        result = string_to_list(result)
        return result

    def GetNameListByMarketAsList(self, market: Optional[Union[str, int]] = None):
        codes = self.GetCodeListByMarketAsList(market)
        names = [self.GetMasterCodeName(code) for code in codes]
        return names

    def GetUserId(self):
        userid = self.GetLoginInfo("USER_ID")
        return userid

    def GetUserName(self):
        username = self.GetLoginInfo("USER_NAME")
        return username

    def GetAccountCount(self):
        account_count = self.GetLoginInfo("ACCOUNT_CNT")
        account_count = int(account_count)
        return account_count

    def GetAccountList(self):
        accounts = self.GetLoginInfo("ACCLIST")
        accounts = string_to_list(accounts)
        return accounts

    def GetKeyboardSecurityStatus(self):
        return self.GetLoginInfo("KEY_BSECGB")

    def IsKeyboardSecurityEnabled(self):
        gubun = self.GetKeyboardSecurityStatus()
        return gubun == "0"

    def GetFirewallStatus(self):
        return self.GetLoginInfo("FIREW_SECGB")

    def IsFirewallEnabled(self):
        gubun = self.GetFirewallStatus()
        return gubun == "1"

    def GetFirstAvailableAccount(self):
        account = None
        accounts = self.GetAccountList()
        if len(accounts) > 0:
            account = accounts[0]
        return account

    def GetMasterStockStateAsList(self, code: str):
        states = self.GetMasterStockState(code).strip()
        states = string_to_list(states, sep="|")
        return states

    def GetKospiCodeList(self):
        codes = self.GetCodeListByMarketAsList("0")
        codes = sorted(codes)
        return codes

    def GetKosdaqCodeList(self):
        codes = self.GetCodeListByMarketAsList("10")
        codes = sorted(codes)
        return codes

    def GetGeneralCodeList(
        self,
        include_preferred_stock: bool = False,
        include_etn: bool = False,
        include_etf: bool = False,
        include_mutual_fund: bool = False,
        include_reits: bool = False,
        include_kosdaq: bool = False,
    ):
        """
        [시장구분값]
          0 : 장내
          10 : 코스닥
          3 : ELW
          8 : ETF
          50 : KONEX
          4 : 뮤추얼펀드
          5 : 신주인수권
          6 : 리츠
          9 : 하이얼펀드
          30 : K-OTC
        """

        codes = self.GetKospiCodeList()

        # 코드 마지막 자리가 0 이 아니면 우선주일 가능성이 있다고 보고 제외
        if not include_preferred_stock:
            codes = [code for code in codes if code.endswith("0")]

        # 장내 시장에서 ETN 이 섞여 있는데 시장구분값으로 뺄 수가 없어서 이름을 보고 대충 제외
        if not include_etn:
            names = [self.GetMasterCodeName(code) for code in codes]
            etn_suffixes = ["ETN", "ETN(H)", "ETN B", "ETN(H) B"]
            is_not_etn_name = [
                not any(name.endswith(suffix) for suffix in etn_suffixes)
                for name in names
            ]
            codes = [code for code, cond in zip(codes, is_not_etn_name) if cond]

        # 코드값 기준 제외 준비
        codes = set(codes)

        # 나머지는 혹시나 겹치는 애들이 나올 수 있는 시장에서 코드기준 제외
        if not include_kosdaq:
            codes = codes - set(self.GetCodeListByMarketAsList("10"))  # 코스닥
        if not include_etf:
            codes = codes - set(self.GetCodeListByMarketAsList("8"))  # ETF
        if not include_mutual_fund:
            codes = codes - set(self.GetCodeListByMarketAsList("4"))  # 뮤추얼펀드
        if not include_reits:
            codes = codes - set(self.GetCodeListByMarketAsList("6"))  # 리츠

        # 정렬된 리스트 형태로 제공
        codes = sorted(list(codes))

        return codes

    def GetStockStates(self, code: str):
        return self.GetMasterStockStateAsList(code)

    def GetSurveillanceFlag(self, code: str):
        return self.GetMasterConstruction(code)

    def IsSuspended(self, code: str):
        return "거래정지" in self.GetMasterStockStateAsList(code)

    def IsUnderSurveillance(self, code: str):
        return "감리종목" in self.GetMasterStockStateAsList(code)

    def IsUnderAdministration(self, code: str):
        return "관리종목" in self.GetMasterStockStateAsList(code)

    def IsFlaggedForCaution(self, code: str):
        flag = self.GetSurveillanceFlag(code)
        states = self.GetMasterStockStateAsList(code)
        flag_is_not_normal = flag != "정상"
        has_caution_state = "투자유의종목" in states
        return flag_is_not_normal or has_caution_state

    def IsNotNormal(self, code: str):
        flag = self.GetSurveillanceFlag(code)
        states = self.GetMasterStockStateAsList(code)
        flag_is_not_normal = flag != "정상"
        bad_states = ["거래정지", "감리종목", "관리종목", "투자유의종목"]
        has_any_bad_state = any(state in states for state in bad_states)
        return flag_is_not_normal or has_any_bad_state

    def IsNormal(self, code: str):
        return not self.IsNotNormal(code)

    def GetConditionFilePath(self):
        module_path = self.GetAPIModulePath()
        userid = self.GetUserId()
        condition_filepath = os.path.join(
            module_path, "system", "%s_NewSaveIndex.dat" % userid
        )
        return condition_filepath

    def GetConditionNameListAsList(self):
        self.EnsureConditionLoaded()
        conditions = self.GetConditionNameList()
        conditions = string_to_list(conditions)
        conditions = [string_to_list(cond, sep="^") for cond in conditions]
        conditions = [(int(cond[0]), cond[1]) for cond in conditions]
        return conditions

    def GetAutoLoginDatPath(self):
        module_path = self.GetAPIModulePath()
        autologin_dat = os.path.join(module_path, "system", "Autologin.dat")
        return autologin_dat

    def IsAutoLoginEnabled(self):
        autologin_dat = self.GetAutoLoginDatPath()
        return os.path.exists(autologin_dat)

    def DisableAutoLogin(self):
        autologin_dat = self.GetAutoLoginDatPath()
        if os.path.exists(autologin_dat):
            os.remove(autologin_dat)

    # ======================================================================

    @classmethod
    def LoginUsingPywinauto_Impl(cls, credentials: Optional[Mapping[str, Any]] = None):
        import pywinauto

        if credentials is None:
            credentials = config.get("koapy.backend.kiwoom_open_api_plus.credentials")

        is_in_development = False
        use_set_text = False

        userid = credentials.get("user_id")
        password = credentials.get("user_password")
        cert = credentials.get("cert_password")

        is_save_userid = True
        is_simulation = credentials.get("is_simulation")

        desktop = pywinauto.Desktop(allow_magic_lookup=False)
        login_window = desktop.window(title="Open API Login")

        try:
            cls.logger.info("Waiting for login screen")
            timeout_login_screen_ready = 30
            login_window.wait("ready", timeout_login_screen_ready)
        except pywinauto.timings.TimeoutError:
            cls.logger.info("Cannot find login screen")
            raise
        else:
            cls.logger.info("Login screen found")
            if is_in_development:
                login_window.print_control_identifiers()

            if userid:
                cls.logger.info("Putting userid")
                if use_set_text:
                    login_window["Edit1"].set_text(userid)
                else:
                    login_window["Edit1"].set_focus()
                    pywinauto.keyboard.send_keys(userid)
                    pywinauto.keyboard.send_keys("{TAB}")
            if password:
                cls.logger.info("Putting password")
                if use_set_text:
                    login_window["Edit2"].set_text(password)
                else:
                    login_window["Edit2"].set_focus()
                    pywinauto.keyboard.send_keys(password)
                    pywinauto.keyboard.send_keys("{TAB}")
            else:
                raise RuntimeError("'user_password' not set, please check credentials")

            if is_save_userid:
                cls.logger.info("Checking to save userid")
                login_window["Button6"].check()  # check doesn't work
            else:
                cls.logger.info("Unchecking to save userid")
                login_window["Button6"].uncheck()  # uncheck doesn't work

            if not is_simulation:
                if not login_window["Edit3"].is_enabled():
                    cls.logger.info("Unchecking to use simulation server")
                    login_window["Button5"].uncheck_by_click()
                if cert:
                    cls.logger.info("Putting cert password")
                    if use_set_text:
                        login_window["Edit3"].set_text(cert)
                    else:
                        login_window["Edit3"].set_focus()
                        pywinauto.keyboard.send_keys(cert)
                        pywinauto.keyboard.send_keys("{TAB}")
                else:
                    raise RuntimeError(
                        "'cert_password' not set, please check credentials"
                    )
            else:
                if login_window["Edit3"].is_enabled():
                    cls.logger.info("Checking to use simulation server")
                    login_window["Button5"].check_by_click()

            cls.logger.info("Logging in")
            login_window["Button1"].click()

    @classmethod
    def LoginUsingPywinauto_RunScriptInSubprocess(
        cls,
        credentials: Optional[Mapping[str, Any]] = None,
        wait: bool = False,
        timeout: bool = None,
        check: bool = False,
    ):
        def main():
            # pylint: disable=redefined-outer-name,reimported,import-self
            import json
            import sys

            from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin import (
                KiwoomOpenApiPlusQAxWidgetMixin,
            )

            credentials = json.load(sys.stdin)
            KiwoomOpenApiPlusQAxWidgetMixin.LoginUsingPywinauto_Impl(credentials)

        args = function_to_subprocess_args(main)
        process = subprocess.Popen(args, stdin=subprocess.PIPE, text=True)
        json.dump(credentials, process.stdin)

        if wait:
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired as exc:
                process.kill()
                exc.stdout, exc.stderr = process.communicate()
                raise exc
            except:
                process.kill()
                raise
            retcode = process.poll()
            completed = subprocess.CompletedProcess(
                process.args, retcode, stdout, stderr
            )
            if check:
                completed.check_returncode()
            return completed

        return process

    def LoginUsingPywinauto(
        self,
        credentials: Optional[Mapping[str, Any]] = None,
        wait: bool = True,
        timeout: bool = None,
        check: bool = True,
    ):
        assert is_admin(), "Using pywinauto requires administrator permission"
        return self.LoginUsingPywinauto_RunScriptInSubprocess(
            credentials, wait=wait, timeout=timeout, check=check
        )

    @overload
    def CommConnectAndThen(
        self,
        credentials: Mapping[str, Any],
        callback: Callable[[int], Any],
    ) -> int:
        ...

    @overload
    def CommConnectAndThen(self, credentials: Mapping[str, Any]) -> int:
        ...

    @overload
    def CommConnectAndThen(self, callback: Callable[[int], Any]) -> int:
        ...

    @overload
    def CommConnectAndThen(self) -> int:
        ...

    def CommConnectAndThen(
        self,
        credentials_or_callback=None,
        callback_or_none=None,
    ) -> int:
        credentials = credentials_or_callback
        callback = callback_or_none

        if (
            callback is None
            and credentials is not None
            and not isinstance(credentials, dict)
            and callable(credentials)
        ):
            callback = credentials
            credentials = None

        if credentials is not None:
            assert (
                is_admin()
            ), "CommConnectAndThen() method requires to be run as administrator if credentials is given explicitly"
            self.DisableAutoLogin()
        elif not self.IsAutoLoginEnabled() and is_admin():
            credentials = config.get(
                "koapy.backend.kiwoom_open_api_plus.credentials", None
            )

        def OnEventConnect(errcode):
            self.OnEventConnect.disconnect(OnEventConnect)
            if callable(callback):
                callback(errcode)

        self.OnEventConnect.connect(OnEventConnect)
        errcode = KiwoomOpenApiPlusError.try_or_raise(self.CommConnect())

        if credentials is not None:
            self.LoginUsingPywinauto(credentials, wait=False)

        return errcode

    def Connect(self, credentials: Optional[Mapping[str, Any]] = None) -> int:
        q = queue.Queue()

        def OnEventConnect(errcode):
            q.put(errcode)

        self.CommConnectAndThen(credentials, OnEventConnect)
        errcode = KiwoomOpenApiPlusError.try_or_raise(q.get())

        return errcode

    @overload
    def EnsureConnectedAndThen(
        self,
        credentials: Mapping[str, Any],
        callback: Callable[[int], Any],
    ) -> bool:
        ...

    @overload
    def EnsureConnectedAndThen(self, credentials: Mapping[str, Any]) -> bool:
        ...

    @overload
    def EnsureConnectedAndThen(self, callback: Callable[[int], Any]) -> bool:
        ...

    @overload
    def EnsureConnectedAndThen(self) -> bool:
        ...

    def EnsureConnectedAndThen(
        self, credentials_or_callback=None, callback_or_none=None
    ) -> bool:
        credentials = credentials_or_callback
        callback = callback_or_none

        if (
            callback is None
            and credentials is not None
            and not isinstance(credentials, dict)
            and callable(credentials)
        ):
            callback = credentials
            credentials = None
        is_connected = self.IsConnected()
        if not is_connected:

            def OnEventConnect(errcode):
                if errcode == 0:
                    if callable(callback):
                        callback()

            self.CommConnectAndThen(credentials, OnEventConnect)
        else:
            if callable(callback):
                callback()
        return is_connected

    def EnsureConnected(self, credentials: Optional[Mapping[str, Any]] = None) -> bool:
        is_connected = self.IsConnected()
        if not is_connected:
            self.Connect(credentials)
            is_connected = self.IsConnected()
            assert is_connected, "Could not ensure connected"
        return is_connected


class KiwoomOpenApiPlusQAxWidgetServerSideMixin(
    KiwoomOpenApiPlusDispatchFunctions, Logging
):
    def __init__(self):

        """
        [OpenAPI 게시판]
          https://bbn.kiwoom.com/bbn.openAPIQnaBbsList.do

        [조회횟수 제한 관련 가이드]
          - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
          - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
          - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
        """

        """
        [조회제한]
          OpenAPI 조회는 1초당 5회로 제한되며 복수종목 조회와 조건검색 조회 횟수가 합산됩니다.
          가령 1초 동안 시세조회2회 관심종목 1회 조건검색 2회 순서로 조회를 했다면 모두 합쳐서 5회이므로 모두 조회성공하겠지만
          조건검색을 3회 조회하면 맨 마지막 조건검색 조회는 실패하게 됩니다.

        [조건검색 제한]
          조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
        """

        self._comm_rate_limiter = KiwoomOpenApiPlusCommRqDataRateLimiter()
        self._cond_rate_limiter = KiwoomOpenApiPlusSendConditionRateLimiter(
            self._comm_rate_limiter
        )
        self._order_rate_limiter = KiwoomOpenApiPlusSendOrderRateLimiter()

        self._comm_rate_limited_executor = QRateLimitedExecutor(
            self._comm_rate_limiter, self
        )
        self._cond_rate_limited_executor = QRateLimitedExecutor(
            self._cond_rate_limiter, self
        )
        self._order_rate_limited_executor = QRateLimitedExecutor(
            self._order_rate_limiter, self
        )

        self.RateLimitedCommRqData = self._comm_rate_limited_executor.wrap(
            self.CommRqDataWithInputs
        )
        self.RateLimitedCommKwRqData = self._comm_rate_limited_executor.wrap(
            self.CommKwRqData
        )
        self.RateLimitedSendCondition = self._cond_rate_limited_executor.wrap(
            self.SendCondition
        )
        self.RateLimitedSendOrder = self._order_rate_limited_executor.wrap(
            self.SendOrder
        )

        self._is_condition_loaded = False

        self._comm_rate_limited_executor.start()
        self._cond_rate_limited_executor.start()
        self._order_rate_limited_executor.start()

        self.destroyed.connect(self._comm_rate_limited_executor.shutdown)
        self.destroyed.connect(self._cond_rate_limited_executor.shutdown)
        self.destroyed.connect(self._order_rate_limited_executor.shutdown)

    def LoadCondition(self) -> int:
        q = queue.Queue()

        def OnReceiveConditionVer(ret, msg):
            if not ret:
                q.put(KiwoomOpenApiPlusError(msg))
            else:
                q.put((ret, msg))

        self.OnReceiveConditionVer.connect(OnReceiveConditionVer)
        try:
            return_code = KiwoomOpenApiPlusError.try_or_raise_boolean(
                self.GetConditionLoad(), "Failed to load condition"
            )
            res = q.get()
            if isinstance(res, KiwoomOpenApiPlusError):
                raise res
        except:  # pylint: disable=try-except-raise
            raise
        else:
            if return_code == 1:
                self._is_condition_loaded = True
        finally:
            self.OnReceiveConditionVer.disconnect(OnReceiveConditionVer)
        return return_code

    def IsConditionLoaded(self) -> bool:
        # the original implementation of this function was like the following:
        #   condition_filepath = self.GetConditionFilePath()
        #   return os.path.exists(condition_filepath)
        # this implementation was based on the description of `GetConditionLoad()` function in the official documentation
        # which was like, "the temporary condition file would be deleted on after OCX program exits".
        # but actually it turned out that existence of this file could not guarantee that the condition is actually loaded or not
        # so here we are using entrypoint-wide member variable to remember once the condition is loaded
        return self._is_condition_loaded

    def EnsureConditionLoaded(self, force: bool = False) -> int:
        return_code = 0
        is_condition_loaded = self.IsConditionLoaded()
        if not is_condition_loaded or force:
            return_code = self.LoadCondition()
        else:
            return_code = 1
        assert return_code == 1, "Could not ensure condition loaded"
        return return_code

    def CommRqDataWithInputs(
        self,
        rqname: str,
        trcode: str,
        prevnext: Union[str, int],
        scrnno: str,
        inputs: Optional[Dict[str, str]] = None,
    ) -> int:
        if inputs:
            for k, v in inputs.items():
                self.SetInputValue(k, v)
        prevnext = int(prevnext)  # ensure prevnext is int
        code = self.CommRqData(rqname, trcode, prevnext, scrnno)
        return code

    @synchronized
    def AtomicCommRqData(
        self,
        rqname: str,
        trcode: str,
        prevnext: Union[str, int],
        scrnno: str,
        inputs: Optional[Dict[str, str]] = None,
    ) -> int:
        return self.CommRqDataWithInputs(rqname, trcode, prevnext, scrnno, inputs)


class KiwoomOpenApiPlusQAxWidgetMixin(
    KiwoomOpenApiPlusQAxWidgetUniversalMixin, KiwoomOpenApiPlusQAxWidgetServerSideMixin
):

    pass
