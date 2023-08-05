# pylint:disable=line-too-long
import logging

from ...sim_type import SimTypeFunction,     SimTypeShort, SimTypeInt, SimTypeLong, SimTypeLongLong, SimTypeDouble, SimTypeFloat,     SimTypePointer,     SimTypeChar,     SimStruct,     SimTypeFixedSizeArray,     SimTypeBottom,     SimUnion,     SimTypeBool
from ...calling_conventions import SimCCStdcall, SimCCMicrosoftAMD64
from .. import SIM_PROCEDURES as P
from . import SimLibrary


_l = logging.getLogger(name=__name__)


lib = SimLibrary()
lib.set_default_cc('X86', SimCCStdcall)
lib.set_default_cc('AMD64', SimCCMicrosoftAMD64)
lib.set_library_names("drt.dll")
prototypes = \
    {
        # 
        'DrtOpen': SimTypeFunction([SimTypePointer(SimStruct({"dwSize": SimTypeInt(signed=False, label="UInt32"), "cbKey": SimTypeInt(signed=False, label="UInt32"), "bProtocolMajorVersion": SimTypeChar(label="Byte"), "bProtocolMinorVersion": SimTypeChar(label="Byte"), "ulMaxRoutingAddresses": SimTypeInt(signed=False, label="UInt32"), "pwzDrtInstancePrefix": SimTypePointer(SimTypeChar(label="Char"), offset=0), "hTransport": SimTypePointer(SimTypeBottom(label="Void"), offset=0), "pSecurityProvider": SimTypePointer(SimStruct({"pvContext": SimTypePointer(SimTypeBottom(label="Void"), offset=0), "Attach": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Detach": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "RegisterKey": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "UnregisterKey": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "ValidateAndUnpackPayload": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "SecureAndPackPayload": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "FreeData": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "EncryptData": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "DecryptData": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "GetSerializedCredential": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "ValidateRemoteCredential": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "SignData": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "VerifyData": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)}, name="DRT_SECURITY_PROVIDER", pack=False, align=None), offset=0), "pBootstrapProvider": SimTypePointer(SimStruct({"pvContext": SimTypePointer(SimTypeBottom(label="Void"), offset=0), "Attach": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Detach": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "InitResolve": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "IssueResolve": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "EndResolve": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Register": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Unregister": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)}, name="DRT_BOOTSTRAP_PROVIDER", pack=False, align=None), offset=0), "eSecurityMode": SimTypeInt(signed=False, label="DRT_SECURITY_MODE")}, name="DRT_SETTINGS", pack=False, align=None), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pSettings", "hEvent", "pvContext", "phDrt"]),
        # 
        'DrtClose': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeBottom(label="Void"), arg_names=["hDrt"]),
        # 
        'DrtGetEventDataSize': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hDrt", "pulEventDataLen"]),
        # 
        'DrtGetEventData': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"type": SimTypeInt(signed=False, label="DRT_EVENT_TYPE"), "hr": SimTypeInt(signed=True, label="Int32"), "pvContext": SimTypePointer(SimTypeBottom(label="Void"), offset=0), "Anonymous": SimUnion({"leafsetKeyChange": SimStruct({"change": SimTypeInt(signed=False, label="DRT_LEAFSET_KEY_CHANGE_TYPE"), "localKey": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), "remoteKey": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None)}, name="_leafsetKeyChange_e__Struct", pack=False, align=None), "registrationStateChange": SimStruct({"state": SimTypeInt(signed=False, label="DRT_REGISTRATION_STATE"), "localKey": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None)}, name="_registrationStateChange_e__Struct", pack=False, align=None), "statusChange": SimStruct({"status": SimTypeInt(signed=False, label="DRT_STATUS"), "bootstrapAddresses": SimStruct({"cntAddress": SimTypeInt(signed=False, label="UInt32"), "pAddresses": SimTypePointer(SimStruct({"ss_family": SimTypeShort(signed=False, label="UInt16"), "__ss_pad1": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 6), "__ss_align": SimTypeLongLong(signed=True, label="Int64"), "__ss_pad2": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 112)}, name="SOCKADDR_STORAGE", pack=False, align=None), offset=0)}, name="_bootstrapAddresses_e__Struct", pack=False, align=None)}, name="_statusChange_e__Struct", pack=False, align=None)}, name="<anon>", label="None")}, name="DRT_EVENT_DATA", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hDrt", "ulEventDataLen", "pEventData"]),
        # 
        'DrtRegisterKey': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimStruct({"key": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), "appData": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None)}, name="DRT_REGISTRATION", pack=False, align=None), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hDrt", "pRegistration", "pvKeyContext", "phKeyRegistration"]),
        # 
        'DrtUpdateKey': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hKeyRegistration", "pAppData"]),
        # 
        'DrtUnregisterKey': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeBottom(label="Void"), arg_names=["hKeyRegistration"]),
        # 
        'DrtStartSearch': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), offset=0), SimTypePointer(SimStruct({"dwSize": SimTypeInt(signed=False, label="UInt32"), "fIterative": SimTypeInt(signed=True, label="Int32"), "fAllowCurrentInstanceMatch": SimTypeInt(signed=True, label="Int32"), "fAnyMatchInRange": SimTypeInt(signed=True, label="Int32"), "cMaxEndpoints": SimTypeInt(signed=False, label="UInt32"), "pMaximumKey": SimTypePointer(SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), offset=0), "pMinimumKey": SimTypePointer(SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), offset=0)}, name="DRT_SEARCH_INFO", pack=False, align=None), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hDrt", "pKey", "pInfo", "timeout", "hEvent", "pvContext", "hSearchContext"]),
        # 
        'DrtContinueSearch': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSearchContext"]),
        # 
        'DrtGetSearchResultSize': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSearchContext", "pulSearchResultSize"]),
        # 
        'DrtGetSearchResult': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"dwSize": SimTypeInt(signed=False, label="UInt32"), "type": SimTypeInt(signed=False, label="DRT_MATCH_TYPE"), "pvContext": SimTypePointer(SimTypeBottom(label="Void"), offset=0), "registration": SimStruct({"key": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None), "appData": SimStruct({"cb": SimTypeInt(signed=False, label="UInt32"), "pb": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="DRT_DATA", pack=False, align=None)}, name="DRT_REGISTRATION", pack=False, align=None)}, name="DRT_SEARCH_RESULT", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSearchContext", "ulSearchResultSize", "pSearchResult"]),
        # 
        'DrtGetSearchPathSize': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSearchContext", "pulSearchPathSize"]),
        # 
        'DrtGetSearchPath': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"AddressCount": SimTypeInt(signed=False, label="UInt32"), "AddressList": SimTypePointer(SimStruct({"socketAddress": SimStruct({"ss_family": SimTypeShort(signed=False, label="UInt16"), "__ss_pad1": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 6), "__ss_align": SimTypeLongLong(signed=True, label="Int64"), "__ss_pad2": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 112)}, name="SOCKADDR_STORAGE", pack=False, align=None), "flags": SimTypeInt(signed=False, label="UInt32"), "nearness": SimTypeInt(signed=True, label="Int32"), "latency": SimTypeInt(signed=False, label="UInt32")}, name="DRT_ADDRESS", pack=False, align=None), offset=0)}, name="DRT_ADDRESS_LIST", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSearchContext", "ulSearchPathSize", "pSearchPath"]),
        # 
        'DrtEndSearch': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSearchContext"]),
        # 
        'DrtGetInstanceName': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeChar(label="Char"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hDrt", "ulcbInstanceNameSize", "pwzDrtInstanceName"]),
        # 
        'DrtGetInstanceNameSize': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hDrt", "pulcbInstanceNameSize"]),
    }

lib.set_prototypes(prototypes)
