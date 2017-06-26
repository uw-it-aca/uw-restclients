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
from uw_trumba.util import fdao_trumba_override, fdao_trumba_sea_override \
                        fdao_trumba_bot_override, fdao_trumba_tac_override


FBOOK = 'restclients.dao_implementation.book.File'
fdao_bookstore_override = override_settings(RESTCLIENTS_BOOK_DAO_CLASS=FBOOK)

FGRAD = 'restclients.dao_implementation.grad.File'
fdao_grad_override = override_settings(RESTCLIENTS_GRAD_DAO_CLASS=FGRAD)

FHFS = 'restclients.dao_implementation.hfs.File'
fdao_hfs_override = override_settings(RESTCLIENTS_HFS_DAO_CLASS=FHFS)

FHRP = 'restclients.dao_implementation.hrpws.File'
fdao_hrp_override = override_settings(RESTCLIENTS_HRPWS_DAO_CLASS=FHRP)

FIAS = 'restclients.dao_implementation.iasystem.File'
fdao_ias_override = override_settings(RESTCLIENTS_IASYSTEM_DAO_CLASS=FIAS)

FUWNETID = 'restclients.dao_implementation.uwnetid.File'
fdao_uwnetid_override = override_settings(
    RESTCLIENTS_UWNETID_DAO_CLASS=FUWNETID)

FMAILMAN = 'restclients.dao_implementation.mailman.File'
fdao_mailman_override = override_settings(
    RESTCLIENTS_MAILMAN_DAO_CLASS=FMAILMAN)

FUPASS = 'restclients.dao_implementation.upass.File'
fdao_upass_override = override_settings(
    RESTCLIENTS_UPASS_DAO_CLASS=FUPASS)
