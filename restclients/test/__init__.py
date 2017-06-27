from django.test.utils import override_settings
from uw_pws.util import fdao_pws_override
from uw_gws.utilities import fdao_gws_override
from uw_sws.util import fdao_sws_override
from uw_kws.utilities import fdao_kws_override
from uw_canvas.utilities import fdao_canvas_override
from uw_libraries.util import (
    fdao_mylib_override as fdao_libacc_override,
    fdao_subject_guide_override as fdao_libcurr_override)
from uw_bridge.util import fdao_bridge_override
from uw_bookstore.util import fdao_bookstore_override

FGRAD = 'restclients.dao_implementation.grad.File'
fdao_grad_override = override_settings(RESTCLIENTS_GRAD_DAO_CLASS=FGRAD)

FHFS = 'restclients.dao_implementation.hfs.File'
fdao_hfs_override = override_settings(RESTCLIENTS_HFS_DAO_CLASS=FHFS)

FHRP = 'restclients.dao_implementation.hrpws.File'
fdao_hrp_override = override_settings(RESTCLIENTS_HRPWS_DAO_CLASS=FHRP)

FIAS = 'restclients.dao_implementation.iasystem.File'
fdao_ias_override = override_settings(RESTCLIENTS_IASYSTEM_DAO_CLASS=FIAS)

FTRUMBA = 'restclients.dao_implementation.trumba.CalendarFile'
fdao_trumba_override = override_settings(
    RESTCLIENTS_CALENDAR_DAO_CLASS=FTRUMBA)

FTRUMBA_SEA = 'restclients.dao_implementation.trumba.FileSea'
fdao_trumba_sea_override = override_settings(
    RESTCLIENTS_TRUMBA_SEA_DAO_CLASS=FTRUMBA_SEA)

FTRUMBA_BOT = 'restclients.dao_implementation.trumba.FileBot'
fdao_trumba_bot_override = override_settings(
    RESTCLIENTS_TRUMBA_BOT_DAO_CLASS=FTRUMBA_BOT)

FTRUMBA_TAC = 'restclients.dao_implementation.trumba.FileTac'
fdao_trumba_tac_override = override_settings(
    RESTCLIENTS_TRUMBA_TAC_DAO_CLASS=FTRUMBA_TAC)

FUWNETID = 'restclients.dao_implementation.uwnetid.File'
fdao_uwnetid_override = override_settings(
    RESTCLIENTS_UWNETID_DAO_CLASS=FUWNETID)

FMAILMAN = 'restclients.dao_implementation.mailman.File'
fdao_mailman_override = override_settings(
    RESTCLIENTS_MAILMAN_DAO_CLASS=FMAILMAN)

FUPASS = 'restclients.dao_implementation.upass.File'
fdao_upass_override = override_settings(
    RESTCLIENTS_UPASS_DAO_CLASS=FUPASS)
