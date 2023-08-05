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
lib.set_library_names("userenv.dll")
prototypes = \
    {
        # 
        'CreateAppContainerProfile': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimStruct({"Sid": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Attributes": SimTypeInt(signed=False, label="UInt32")}, name="SID_AND_ATTRIBUTES", pack=False, align=None), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pszAppContainerName", "pszDisplayName", "pszDescription", "pCapabilities", "dwCapabilityCount", "ppSidAppContainerSid"]),
        # 
        'DeleteAppContainerProfile': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pszAppContainerName"]),
        # 
        'GetAppContainerRegistryLocation': SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["desiredAccess", "phAppContainerKey"]),
        # 
        'GetAppContainerFolderPath': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pszAppContainerSid", "ppszPath"]),
        # 
        'DeriveAppContainerSidFromAppContainerName': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pszAppContainerName", "ppsidAppContainerSid"]),
        # 
        'DeriveRestrictedAppContainerSidFromAppContainerSidAndRestrictedName': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["psidAppContainerSid", "pszRestrictedAppContainerName", "ppsidRestrictedAppContainerSid"]),
        # 
        'CreateEnvironmentBlock': SimTypeFunction([SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=True, label="Int32")], SimTypeInt(signed=True, label="Int32"), arg_names=["lpEnvironment", "hToken", "bInherit"]),
        # 
        'DestroyEnvironmentBlock': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpEnvironment"]),
        # 
        'ExpandEnvironmentStringsForUserA': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeChar(label="Byte"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpSrc", "lpDest", "dwSize"]),
        # 
        'ExpandEnvironmentStringsForUserW': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpSrc", "lpDest", "dwSize"]),
        # 
        'RefreshPolicy': SimTypeFunction([SimTypeInt(signed=True, label="Int32")], SimTypeInt(signed=True, label="Int32"), arg_names=["bMachine"]),
        # 
        'RefreshPolicyEx': SimTypeFunction([SimTypeInt(signed=True, label="Int32"), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["bMachine", "dwOptions"]),
        # 
        'EnterCriticalPolicySection': SimTypeFunction([SimTypeInt(signed=True, label="Int32")], SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), arg_names=["bMachine"]),
        # 
        'LeaveCriticalPolicySection': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSection"]),
        # 
        'RegisterGPNotification': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=True, label="Int32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hEvent", "bMachine"]),
        # 
        'UnregisterGPNotification': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hEvent"]),
        # 
        'GetGPOListA': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimStruct({"dwOptions": SimTypeInt(signed=False, label="UInt32"), "dwVersion": SimTypeInt(signed=False, label="UInt32"), "lpDSPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpFileSysPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpDisplayName": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "szGPOName": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 50), "GPOLink": SimTypeInt(signed=False, label="GPO_LINK"), "lParam": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "pNext": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTA"), offset=0), "pPrev": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTA"), offset=0), "lpExtensions": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lParam2": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "lpLink": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="GROUP_POLICY_OBJECTA", pack=False, align=None), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpName", "lpHostName", "lpComputerName", "dwFlags", "pGPOList"]),
        # 
        'GetGPOListW': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimStruct({"dwOptions": SimTypeInt(signed=False, label="UInt32"), "dwVersion": SimTypeInt(signed=False, label="UInt32"), "lpDSPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpFileSysPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpDisplayName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "szGPOName": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 50), "GPOLink": SimTypeInt(signed=False, label="GPO_LINK"), "lParam": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "pNext": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTW"), offset=0), "pPrev": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTW"), offset=0), "lpExtensions": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lParam2": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "lpLink": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="GROUP_POLICY_OBJECTW", pack=False, align=None), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpName", "lpHostName", "lpComputerName", "dwFlags", "pGPOList"]),
        # 
        'FreeGPOListA': SimTypeFunction([SimTypePointer(SimStruct({"dwOptions": SimTypeInt(signed=False, label="UInt32"), "dwVersion": SimTypeInt(signed=False, label="UInt32"), "lpDSPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpFileSysPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpDisplayName": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "szGPOName": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 50), "GPOLink": SimTypeInt(signed=False, label="GPO_LINK"), "lParam": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "pNext": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTA"), offset=0), "pPrev": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTA"), offset=0), "lpExtensions": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lParam2": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "lpLink": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="GROUP_POLICY_OBJECTA", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pGPOList"]),
        # 
        'FreeGPOListW': SimTypeFunction([SimTypePointer(SimStruct({"dwOptions": SimTypeInt(signed=False, label="UInt32"), "dwVersion": SimTypeInt(signed=False, label="UInt32"), "lpDSPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpFileSysPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpDisplayName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "szGPOName": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 50), "GPOLink": SimTypeInt(signed=False, label="GPO_LINK"), "lParam": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "pNext": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTW"), offset=0), "pPrev": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTW"), offset=0), "lpExtensions": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lParam2": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "lpLink": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="GROUP_POLICY_OBJECTW", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pGPOList"]),
        # 
        'GetAppliedGPOListA': SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Guid"), offset=0), SimTypePointer(SimTypePointer(SimStruct({"dwOptions": SimTypeInt(signed=False, label="UInt32"), "dwVersion": SimTypeInt(signed=False, label="UInt32"), "lpDSPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpFileSysPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpDisplayName": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "szGPOName": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 50), "GPOLink": SimTypeInt(signed=False, label="GPO_LINK"), "lParam": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "pNext": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTA"), offset=0), "pPrev": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTA"), offset=0), "lpExtensions": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lParam2": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "lpLink": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="GROUP_POLICY_OBJECTA", pack=False, align=None), offset=0), offset=0)], SimTypeInt(signed=False, label="UInt32"), arg_names=["dwFlags", "pMachineName", "pSidUser", "pGuidExtension", "ppGPOList"]),
        # 
        'GetAppliedGPOListW': SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Guid"), offset=0), SimTypePointer(SimTypePointer(SimStruct({"dwOptions": SimTypeInt(signed=False, label="UInt32"), "dwVersion": SimTypeInt(signed=False, label="UInt32"), "lpDSPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpFileSysPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpDisplayName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "szGPOName": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 50), "GPOLink": SimTypeInt(signed=False, label="GPO_LINK"), "lParam": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "pNext": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTW"), offset=0), "pPrev": SimTypePointer(SimTypeBottom(label="GROUP_POLICY_OBJECTW"), offset=0), "lpExtensions": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lParam2": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "lpLink": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="GROUP_POLICY_OBJECTW", pack=False, align=None), offset=0), offset=0)], SimTypeInt(signed=False, label="UInt32"), arg_names=["dwFlags", "pMachineName", "pSidUser", "pGuidExtension", "ppGPOList"]),
        # 
        'ProcessGroupPolicyCompleted': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Guid"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt"), label="UIntPtr", offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=False, label="UInt32"), arg_names=["extensionId", "pAsyncHandle", "dwStatus"]),
        # 
        'ProcessGroupPolicyCompletedEx': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Guid"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt"), label="UIntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=True, label="Int32")], SimTypeInt(signed=False, label="UInt32"), arg_names=["extensionId", "pAsyncHandle", "dwStatus", "RsopStatus"]),
        # 
        'RsopAccessCheckByType': SimTypeFunction([SimTypePointer(SimStruct({"Revision": SimTypeChar(label="Byte"), "Sbz1": SimTypeChar(label="Byte"), "Control": SimTypeShort(signed=False, label="UInt16"), "Owner": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Group": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), "Sacl": SimTypePointer(SimStruct({"AclRevision": SimTypeChar(label="Byte"), "Sbz1": SimTypeChar(label="Byte"), "AclSize": SimTypeShort(signed=False, label="UInt16"), "AceCount": SimTypeShort(signed=False, label="UInt16"), "Sbz2": SimTypeShort(signed=False, label="UInt16")}, name="ACL", pack=False, align=None), offset=0), "Dacl": SimTypePointer(SimStruct({"AclRevision": SimTypeChar(label="Byte"), "Sbz1": SimTypeChar(label="Byte"), "AclSize": SimTypeShort(signed=False, label="UInt16"), "AceCount": SimTypeShort(signed=False, label="UInt16"), "Sbz2": SimTypeShort(signed=False, label="UInt16")}, name="ACL", pack=False, align=None), offset=0)}, name="SECURITY_DESCRIPTOR", pack=False, align=None), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"Level": SimTypeShort(signed=False, label="UInt16"), "Sbz": SimTypeShort(signed=False, label="UInt16"), "ObjectType": SimTypePointer(SimTypeBottom(label="Guid"), offset=0)}, name="OBJECT_TYPE_LIST", pack=False, align=None), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"GenericRead": SimTypeInt(signed=False, label="UInt32"), "GenericWrite": SimTypeInt(signed=False, label="UInt32"), "GenericExecute": SimTypeInt(signed=False, label="UInt32"), "GenericAll": SimTypeInt(signed=False, label="UInt32")}, name="GENERIC_MAPPING", pack=False, align=None), offset=0), SimTypePointer(SimStruct({"PrivilegeCount": SimTypeInt(signed=False, label="UInt32"), "Control": SimTypeInt(signed=False, label="UInt32"), "Privilege": SimTypePointer(SimStruct({"Luid": SimTypeBottom(label="LUID"), "Attributes": SimTypeInt(signed=False, label="TOKEN_PRIVILEGES_ATTRIBUTES")}, name="LUID_AND_ATTRIBUTES", pack=False, align=None), offset=0)}, name="PRIVILEGE_SET", pack=False, align=None), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pSecurityDescriptor", "pPrincipalSelfSid", "pRsopToken", "dwDesiredAccessMask", "pObjectTypeList", "ObjectTypeListLength", "pGenericMapping", "pPrivilegeSet", "pdwPrivilegeSetLength", "pdwGrantedAccessMask", "pbAccessStatus"]),
        # 
        'RsopFileAccessCheck': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pszFileName", "pRsopToken", "dwDesiredAccessMask", "pdwGrantedAccessMask", "pbAccessStatus"]),
        # 
        'RsopSetPolicySettingStatus': SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypeBottom(label="IWbemServices"), SimTypeBottom(label="IWbemClassObject"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"szKey": SimTypePointer(SimTypeChar(label="Char"), offset=0), "szEventSource": SimTypePointer(SimTypeChar(label="Char"), offset=0), "szEventLogName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "dwEventID": SimTypeInt(signed=False, label="UInt32"), "dwErrorCode": SimTypeInt(signed=False, label="UInt32"), "status": SimTypeInt(signed=False, label="SETTINGSTATUS"), "timeLogged": SimStruct({"wYear": SimTypeShort(signed=False, label="UInt16"), "wMonth": SimTypeShort(signed=False, label="UInt16"), "wDayOfWeek": SimTypeShort(signed=False, label="UInt16"), "wDay": SimTypeShort(signed=False, label="UInt16"), "wHour": SimTypeShort(signed=False, label="UInt16"), "wMinute": SimTypeShort(signed=False, label="UInt16"), "wSecond": SimTypeShort(signed=False, label="UInt16"), "wMilliseconds": SimTypeShort(signed=False, label="UInt16")}, name="SYSTEMTIME", pack=False, align=None)}, name="POLICYSETTINGSTATUSINFO", pack=False, align=None), label="LPArray", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["dwFlags", "pServices", "pSettingInstance", "nInfo", "pStatus"]),
        # 
        'RsopResetPolicySettingStatus': SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypeBottom(label="IWbemServices"), SimTypeBottom(label="IWbemClassObject")], SimTypeInt(signed=True, label="Int32"), arg_names=["dwFlags", "pServices", "pSettingInstance"]),
        # 
        'GenerateGPNotification': SimTypeFunction([SimTypeInt(signed=True, label="Int32"), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=False, label="UInt32"), arg_names=["bMachine", "lpwszMgmtProduct", "dwMgmtProductOptions"]),
        # 
        'LoadUserProfileA': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"dwSize": SimTypeInt(signed=False, label="UInt32"), "dwFlags": SimTypeInt(signed=False, label="UInt32"), "lpUserName": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpProfilePath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpDefaultPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpServerName": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "lpPolicyPath": SimTypePointer(SimTypeChar(label="Byte"), offset=0), "hProfile": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)}, name="PROFILEINFOA", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpProfileInfo"]),
        # 
        'LoadUserProfileW': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"dwSize": SimTypeInt(signed=False, label="UInt32"), "dwFlags": SimTypeInt(signed=False, label="UInt32"), "lpUserName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpProfilePath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpDefaultPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpServerName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "lpPolicyPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "hProfile": SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)}, name="PROFILEINFOW", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpProfileInfo"]),
        # 
        'UnloadUserProfile': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "hProfile"]),
        # 
        'GetProfilesDirectoryA': SimTypeFunction([SimTypePointer(SimTypeChar(label="Byte"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpProfileDir", "lpcchSize"]),
        # 
        'GetProfilesDirectoryW': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpProfileDir", "lpcchSize"]),
        # 
        'GetProfileType': SimTypeFunction([SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["dwFlags"]),
        # 
        'DeleteProfileA': SimTypeFunction([SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpSidString", "lpProfilePath", "lpComputerName"]),
        # 
        'DeleteProfileW': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpSidString", "lpProfilePath", "lpComputerName"]),
        # 
        'CreateProfile': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["pszUserSid", "pszUserName", "pszProfilePath", "cchProfilePath"]),
        # 
        'GetDefaultUserProfileDirectoryA': SimTypeFunction([SimTypePointer(SimTypeChar(label="Byte"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpProfileDir", "lpcchSize"]),
        # 
        'GetDefaultUserProfileDirectoryW': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpProfileDir", "lpcchSize"]),
        # 
        'GetAllUsersProfileDirectoryA': SimTypeFunction([SimTypePointer(SimTypeChar(label="Byte"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpProfileDir", "lpcchSize"]),
        # 
        'GetAllUsersProfileDirectoryW': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpProfileDir", "lpcchSize"]),
        # 
        'GetUserProfileDirectoryA': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Byte"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpProfileDir", "lpcchSize"]),
        # 
        'GetUserProfileDirectoryW': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hToken", "lpProfileDir", "lpcchSize"]),
    }

lib.set_prototypes(prototypes)
