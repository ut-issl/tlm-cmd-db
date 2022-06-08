# SAMPLE_MOBC_TLM_DB_HK

Name|Type|Exp.|Octet Pos.|bit Pos.|bit Len.|HEX|Status|a0|a1|a2|a3|a4|a5|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
PH.VER|uint16_t||0|0|3|||||||||||
PH.TYPE|||0|3|1|||||||||||
PH.SH_FLAG|||0|4|1|||||||||||
PH.APID|||0|5|11|||||||||||
PH.SEQ_FLAG|uint16_t||2|0|2|||||||||||
PH.SEQ_COUNT|||2|2|14|||||||||||
PH.PACKET_LEN|uint16_t||4|0|16|||||||||||
SH.VER|uint8_t||6|0|8|||||||||||
SH.TI|uint32_t||7|0|32|||||||||||
SH.TLM_ID|uint8_t||11|0|8|o||||||||||
SH.GLOBAL_TIME|double||12|0|64|||||||||||
SH.ON_BOARD_SUBNET_TIME|uint32_t||20|0|32|||||||||||
SH.DEST_FLAGS|uint8_t||24|0|8|o||||||||||
SH.DR_PARTITION|uint8_t||25|0|8|||||||||||
OBC_TCP_LAST_RECV_ACK|uint8_t|(uint8_t)(gs_driver->latest_info->rx.cmd_ack)|26|0|8||13.1|||||||最新TCPacket受信処理結果|メモ|
OBC_MM_STS|uint8_t||27|0|1||2.5|||||||||
OBC_MM_OPSMODE_PREV|||27|1|7||17.1|||||||||
CMD0_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 0)|28|0|16|o||||||||||
CMD0_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 0)|30|0|32|||||||||||
CMD1_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 1)|34|0|16|o||||||||||
CMD1_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 1)|36|0|32|||||||||||
CMD2_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 2)|40|0|16|o||||||||||
CMD2_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 2)|42|0|32|||||||||||
CMD3_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 3)|46|0|16|o||||||||||
CMD3_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 3)|48|0|32|||||||||||
CMD4_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 4)|52|0|16|o||||||||||
CMD4_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 4)|54|0|32|||||||||||
CMD5_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 5)|58|0|16|o||||||||||
CMD5_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 5)|60|0|32|||||||||||
CMD6_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 6)|64|0|16|o||||||||||
CMD6_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 6)|66|0|32|||||||||||
CMD7_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 7)|70|0|16|o||||||||||
CMD7_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 7)|72|0|32|||||||||||
CMD8_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 8)|76|0|16|o||||||||||
CMD8_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 8)|78|0|32|||||||||||
CMD9_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 9)|82|0|16|o||||||||||
CMD9_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 9)|84|0|32|||||||||||
CMD10_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 10)|88|0|16|o||||||||||
CMD10_TI|uint32_t|(uint32_t)BCT_get_ti(block_command_table->pos.block, 10)|90|0|32|||||||||||
EL_EVENT_COUNTER.COUNTERS.EL_ERROR_LEVEL_HIGH|uint32_t|event_handler->el_event_counter.counters[EL_ERROR_LEVEL_HIGH]|94|0|32|||||||||||
EL_EVENT_COUNTER.COUNTERS.EL_ERROR_LEVEL_MIDDLE|uint32_t|event_handler->el_event_counter.counters[EL_ERROR_LEVEL_MIDDLE]|98|0|32|||||||||||
EL_EVENT_COUNTER.COUNTERS.EL_ERROR_LEVEL_LOW|uint32_t|event_handler->el_event_counter.counters[EL_ERROR_LEVEL_LOW]|102|0|32|||||||||||
EL_EVENT_COUNTER.COUNTERS.EL_ERROR_LEVEL_EL|uint32_t|event_handler->el_event_counter.counters[EL_ERROR_LEVEL_EL]|106|0|32|||||||||||
EL_EVENT_COUNTER.COUNTERS.EL_ERROR_LEVEL_EH|uint32_t|event_handler->el_event_counter.counters[EL_ERROR_LEVEL_EH]|110|0|32|||||||||||
APP_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].initializer)|114|0|32|o||||||||||
APP_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].entry_point)|118|0|32|o||||||||||
APP_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].init_duration)|122|0|8|||||||||||
APP_PREV_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].prev)|123|0|8|||||||||||
APP0_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].initializer)|124|0|32|o||||||||||
APP0_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].entry_point)|128|0|32|o||||||||||
APP0_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].init_duration)|132|0|8|||||||||||
APP1_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].initializer)|133|0|32|o||||||||||
APP1_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].entry_point)|137|0|32|o||||||||||
APP1_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].init_duration)|141|0|8|||||||||||
APP2_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].initializer)|142|0|32|o||||||||||
APP2_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].entry_point)|146|0|32|o||||||||||
APP2_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].init_duration)|150|0|8|||||||||||
APP3_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+3].initializer)|151|0|32|o||||||||||
APP3_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+3].entry_point)|155|0|32|o||||||||||
APP3_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+3].init_duration)|159|0|8|||||||||||
APP4_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+4].initializer)|160|0|32|o||||||||||
APP4_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+4].entry_point)|164|0|32|o||||||||||
APP4_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+4].init_duration)|168|0|8|||||||||||
APP5_INITIALIZER|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+5].initializer)|169|0|32|o||||||||||
APP5_ENTRYPOINT|uint32_t|(uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+5].entry_point)|173|0|32|o||||||||||
APP5_INIT_PROC_TIME|uint8_t|(uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+5].init_duration)|177|0|8|||||||||||
CMD_0_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 0)|178|0|16|o||||||||||
CMD_0_PARAM0|uint8_t|BCT_get_param_head(block_command_table->pos.block, 0)[0]|180|0|8|o||||||||||
CMD_0_PARAM1|uint8_t|BCT_get_param_head(block_command_table->pos.block, 0)[1]|181|0|8|o||||||||||
CMD_0_PARAM2|uint8_t|BCT_get_param_head(block_command_table->pos.block, 0)[2]|182|0|8|o||||||||||
CMD_0_PARAM3|uint8_t|BCT_get_param_head(block_command_table->pos.block, 0)[3]|183|0|8|o||||||||||
CMD_0_PARAM4|uint8_t|BCT_get_param_head(block_command_table->pos.block, 0)[4]|184|0|8|o||||||||||
CMD_0_PARAM5|uint8_t|BCT_get_param_head(block_command_table->pos.block, 0)[5]|185|0|8|o||||||||||
CMD_1_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 1)|186|0|16|o||||||||||
CMD_1_PARAM0|uint8_t|BCT_get_param_head(block_command_table->pos.block, 1)[0]|188|0|8|o||||||||||
CMD_1_PARAM1|uint8_t|BCT_get_param_head(block_command_table->pos.block, 1)[1]|189|0|8|o||||||||||
CMD_1_PARAM2|uint8_t|BCT_get_param_head(block_command_table->pos.block, 1)[2]|190|0|8|o||||||||||
CMD_1_PARAM3|uint8_t|BCT_get_param_head(block_command_table->pos.block, 1)[3]|191|0|8|o||||||||||
CMD_1_PARAM4|uint8_t|BCT_get_param_head(block_command_table->pos.block, 1)[4]|192|0|8|o||||||||||
CMD_1_PARAM5|uint8_t|BCT_get_param_head(block_command_table->pos.block, 1)[5]|193|0|8|o||||||||||
CMD_2_ID|uint16_t|(uint16_t)BCT_get_id(block_command_table->pos.block, 2)|194|0|16|o||||||||||
CMD_2_PARAM0|uint8_t|BCT_get_param_head(block_command_table->pos.block, 2)[0]|196|0|8|o||||||||||
CMD_2_PARAM1|uint8_t|BCT_get_param_head(block_command_table->pos.block, 2)[1]|197|0|8|o||||||||||
CMD_2_PARAM2|uint8_t|BCT_get_param_head(block_command_table->pos.block, 2)[2]|198|0|8|o||||||||||
CMD_2_PARAM3|uint8_t|BCT_get_param_head(block_command_table->pos.block, 2)[3]|199|0|8|o||||||||||
CMD_2_PARAM4|uint8_t|BCT_get_param_head(block_command_table->pos.block, 2)[4]|200|0|8|o||||||||||
CMD_2_PARAM5|uint8_t|BCT_get_param_head(block_command_table->pos.block, 2)[5]|201|0|8|o||||||||||
RULE0.SETTINGS.EVENT.GROUP|uint8_t|(uint8_t)rules[0 + offset].settings.event.group|202|0|8|||||||||||
RULE0.SETTINGS.EVENT.LOCAL|uint32_t|(uint32_t)rules[0 + offset].settings.event.local|203|0|32|||||||||||
RULE0.SETTINGS.EVENT.ERR_LEVEL|uint8_t||207|0|3||5.1|||||||||
RULE0.SETTINGS.SHOULD_MATCH_ERR_LEVEL|||207|3|1||2.5|||||||||
RULE0.SETTINGS.IS_ACTIVE|||207|4|1||2.6|||||||||
RULE0.SETTINGS.CONDITION.TYPE|||207|5|3||3.1|||||||||
RULE1.SETTINGS.EVENT.GROUP|uint8_t|(uint8_t)rules[1 + offset].settings.event.group|208|0|8|||||||||||
RULE1.SETTINGS.EVENT.LOCAL|uint32_t|(uint32_t)rules[1 + offset].settings.event.local|209|0|32|||||||||||
RULE1.SETTINGS.EVENT.ERR_LEVEL|uint8_t||213|0|3||5.1|||||||||
RULE1.SETTINGS.SHOULD_MATCH_ERR_LEVEL|||213|3|1||2.5|||||||||
RULE1.SETTINGS.IS_ACTIVE|||213|4|1||2.6|||||||||
RULE1.SETTINGS.CONDITION.TYPE|||213|5|3||3.1|||||||||
RULE2.SETTINGS.EVENT.GROUP|uint8_t|(uint8_t)rules[2 + offset].settings.event.group|214|0|8|||||||||||
RULE2.SETTINGS.EVENT.LOCAL|uint32_t|(uint32_t)rules[2 + offset].settings.event.local|215|0|32|||||||||||
RULE2.SETTINGS.EVENT.ERR_LEVEL|uint8_t||219|0|3||5.1|||||||||
RULE2.SETTINGS.SHOULD_MATCH_ERR_LEVEL|||219|3|1||2.5|||||||||
RULE2.SETTINGS.IS_ACTIVE|||219|4|1||2.6|||||||||
RULE2.SETTINGS.CONDITION.TYPE|||219|5|3||3.1|||||||||
RULE3.SETTINGS.EVENT.GROUP|uint8_t|(uint8_t)rules[3 + offset].settings.event.group|220|0|8|||||||||||
RULE3.SETTINGS.EVENT.LOCAL|uint32_t|(uint32_t)rules[3 + offset].settings.event.local|221|0|32|||||||||||
RULE3.SETTINGS.EVENT.ERR_LEVEL|uint8_t||225|0|3||5.1|||||||||
RULE3.SETTINGS.SHOULD_MATCH_ERR_LEVEL|||225|3|1||2.5|||||||||
RULE3.SETTINGS.IS_ACTIVE|||225|4|1||2.6|||||||||
RULE3.SETTINGS.CONDITION.TYPE|||225|5|3||3.1|||||||||
RULE4.SETTINGS.EVENT.GROUP|uint8_t|(uint8_t)rules[4 + offset].settings.event.group|226|0|8|||||||||||
RULE4.SETTINGS.EVENT.LOCAL|uint32_t|(uint32_t)rules[4 + offset].settings.event.local|227|0|32|||||||||||
RULE4.SETTINGS.EVENT.ERR_LEVEL|uint8_t||231|0|3||5.1|||||||||
RULE4.SETTINGS.SHOULD_MATCH_ERR_LEVEL|||231|3|1||2.5|||||||||
RULE4.SETTINGS.IS_ACTIVE|||231|4|1||2.6|||||||||
RULE4.SETTINGS.CONDITION.TYPE|||231|5|3||3.1|||||||||
RULE5.SETTINGS.EVENT.GROUP|uint8_t|(uint8_t)rules[5 + offset].settings.event.group|232|0|8|||||||||||
RULE5.SETTINGS.EVENT.LOCAL|uint32_t|(uint32_t)rules[5 + offset].settings.event.local|233|0|32|||||||||||
RULE5.SETTINGS.EVENT.ERR_LEVEL|uint8_t||237|0|3||5.1|||||||||
RULE5.SETTINGS.SHOULD_MATCH_ERR_LEVEL|||237|3|1||2.5|||||||||
RULE5.SETTINGS.IS_ACTIVE|||237|4|1||2.6|||||||||
RULE5.SETTINGS.CONDITION.TYPE|||237|5|3||3.1|||||||||
IS_LOGGING_ENABLE0|uint8_t|event_logger->is_logging_enable[0]|238|0|1|||||||||||
IS_LOGGING_ENABLE1|||238|1|1|||||||||||
IS_LOGGING_ENABLE2|||238|2|1|||||||||||
IS_LOGGING_ENABLE3|||238|3|1|||||||||||
IS_LOGGING_ENABLE4|||238|4|1|||||||||||
IS_LOGGING_ENABLE5|||238|5|1|||||||||||
IS_LOGGING_ENABLE6|||238|6|1|||||||||||
IS_LOGGING_ENABLE7|||238|7|1|||||||||||
IS_LOGGING_ENABLE8|uint8_t|event_logger->is_logging_enable[1]|239|0|1|||||||||||
IS_LOGGING_ENABLE9|||239|1|1|||||||||||
IS_LOGGING_ENABLE10|||239|2|1|||||||||||
IS_LOGGING_ENABLE11|||239|3|1|||||||||||
IS_LOGGING_ENABLE12|||239|4|1|||||||||||
IS_LOGGING_ENABLE13|||239|5|1|||||||||||
IS_LOGGING_ENABLE14|||239|6|1|||||||||||
IS_LOGGING_ENABLE15|||239|7|1|||||||||||
IS_LOGGING_ENABLE16|uint8_t|event_logger->is_logging_enable[2]|240|0|1|||||||||||
IS_LOGGING_ENABLE17|||240|1|1|||||||||||
IS_LOGGING_ENABLE18|||240|2|1|||||||||||
IS_LOGGING_ENABLE19|||240|3|1|||||||||||
IS_LOGGING_ENABLE20|||240|4|1|||||||||||
IS_LOGGING_ENABLE21|||240|5|1|||||||||||
IS_LOGGING_ENABLE22|||240|6|1|||||||||||
IS_LOGGING_ENABLE23|||240|7|1|||||||||||
IS_LOGGING_ENABLE24|uint8_t|event_logger->is_logging_enable[3]|241|0|1|||||||||||
IS_LOGGING_ENABLE25|||241|1|1|||||||||||
IS_LOGGING_ENABLE26|||241|2|1|||||||||||
IS_LOGGING_ENABLE27|||241|3|1|||||||||||
IS_LOGGING_ENABLE28|||241|4|1|||||||||||
IS_LOGGING_ENABLE29|||241|5|1|||||||||||
IS_LOGGING_ENABLE30|||241|6|1|||||||||||
IS_LOGGING_ENABLE31|||241|7|1|||||||||||
TLOGS.HIGH.EVENTS0.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->group|242|0|8|||||||||||
TLOGS.HIGH.EVENTS0.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->local|243|0|32|||||||||||
TLOGS.HIGH.EVENTS0.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->time.total_cycle|247|0|32|||||||||||
TLOGS.HIGH.EVENTS0.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->time.step|251|0|8|||||||||||
TLOGS.HIGH.EVENTS0.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->note|252|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.HIGH.EVENTS1.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->group|256|0|8|||||||||||
TLOGS.HIGH.EVENTS1.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->local|257|0|32|||||||||||
TLOGS.HIGH.EVENTS1.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->time.total_cycle|261|0|32|||||||||||
TLOGS.HIGH.EVENTS1.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->time.step|265|0|8|||||||||||
TLOGS.HIGH.EVENTS1.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->note|266|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.HIGH.EVENTS2.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->group|270|0|8|||||||||||
TLOGS.HIGH.EVENTS2.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->local|271|0|32|||||||||||
TLOGS.HIGH.EVENTS2.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->time.total_cycle|275|0|32|||||||||||
TLOGS.HIGH.EVENTS2.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->time.step|279|0|8|||||||||||
TLOGS.HIGH.EVENTS2.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->note|280|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.HIGH.EVENTS3.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->group|284|0|8|||||||||||
TLOGS.HIGH.EVENTS3.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->local|285|0|32|||||||||||
TLOGS.HIGH.EVENTS3.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->time.total_cycle|289|0|32|||||||||||
TLOGS.HIGH.EVENTS3.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->time.step|293|0|8|||||||||||
TLOGS.HIGH.EVENTS3.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->note|294|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.MIDDLE.EVENTS0.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->group|298|0|8|||||||||||
TLOGS.MIDDLE.EVENTS0.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->local|299|0|32|||||||||||
TLOGS.MIDDLE.EVENTS0.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->time.total_cycle|303|0|32|||||||||||
TLOGS.MIDDLE.EVENTS0.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->time.step|307|0|8|||||||||||
TLOGS.MIDDLE.EVENTS0.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->note|308|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.MIDDLE.EVENTS1.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->group|312|0|8|||||||||||
TLOGS.MIDDLE.EVENTS1.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->local|313|0|32|||||||||||
TLOGS.MIDDLE.EVENTS1.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->time.total_cycle|317|0|32|||||||||||
TLOGS.MIDDLE.EVENTS1.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->time.step|321|0|8|||||||||||
TLOGS.MIDDLE.EVENTS1.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->note|322|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.MIDDLE.EVENTS2.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->group|326|0|8|||||||||||
TLOGS.MIDDLE.EVENTS2.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->local|327|0|32|||||||||||
TLOGS.MIDDLE.EVENTS2.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->time.total_cycle|331|0|32|||||||||||
TLOGS.MIDDLE.EVENTS2.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->time.step|335|0|8|||||||||||
TLOGS.MIDDLE.EVENTS2.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->note|336|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.MIDDLE.EVENTS3.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->group|340|0|8|||||||||||
TLOGS.MIDDLE.EVENTS3.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->local|341|0|32|||||||||||
TLOGS.MIDDLE.EVENTS3.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->time.total_cycle|345|0|32|||||||||||
TLOGS.MIDDLE.EVENTS3.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->time.step|349|0|8|||||||||||
TLOGS.MIDDLE.EVENTS3.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->note|350|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.LOW.EVENTS0.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->group|354|0|8|||||||||||
TLOGS.LOW.EVENTS0.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->local|355|0|32|||||||||||
TLOGS.LOW.EVENTS0.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->time.total_cycle|359|0|32|||||||||||
TLOGS.LOW.EVENTS0.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->time.step|363|0|8|||||||||||
TLOGS.LOW.EVENTS0.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->note|364|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.LOW.EVENTS1.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->group|368|0|8|||||||||||
TLOGS.LOW.EVENTS1.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->local|369|0|32|||||||||||
TLOGS.LOW.EVENTS1.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->time.total_cycle|373|0|32|||||||||||
TLOGS.LOW.EVENTS1.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->time.step|377|0|8|||||||||||
TLOGS.LOW.EVENTS1.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->note|378|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.LOW.EVENTS2.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->group|382|0|8|||||||||||
TLOGS.LOW.EVENTS2.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->local|383|0|32|||||||||||
TLOGS.LOW.EVENTS2.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->time.total_cycle|387|0|32|||||||||||
TLOGS.LOW.EVENTS2.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->time.step|391|0|8|||||||||||
TLOGS.LOW.EVENTS2.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->note|392|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.LOW.EVENTS3.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->group|396|0|8|||||||||||
TLOGS.LOW.EVENTS3.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->local|397|0|32|||||||||||
TLOGS.LOW.EVENTS3.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->time.total_cycle|401|0|32|||||||||||
TLOGS.LOW.EVENTS3.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->time.step|405|0|8|||||||||||
TLOGS.LOW.EVENTS3.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->note|406|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.LOW.EVENTS4.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->group|410|0|8|||||||||||
TLOGS.LOW.EVENTS4.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->local|411|0|32|||||||||||
TLOGS.LOW.EVENTS4.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->time.total_cycle|415|0|32|||||||||||
TLOGS.LOW.EVENTS4.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->time.step|419|0|8|||||||||||
TLOGS.LOW.EVENTS4.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->note|420|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.LOW.EVENTS5.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->group|424|0|8|||||||||||
TLOGS.LOW.EVENTS5.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->local|425|0|32|||||||||||
TLOGS.LOW.EVENTS5.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->time.total_cycle|429|0|32|||||||||||
TLOGS.LOW.EVENTS5.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->time.step|433|0|8|||||||||||
TLOGS.LOW.EVENTS5.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->note|434|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EL.EVENTS0.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->group|438|0|8|||||||||||
TLOGS.EL.EVENTS0.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->local|439|0|32|||||||||||
TLOGS.EL.EVENTS0.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->time.total_cycle|443|0|32|||||||||||
TLOGS.EL.EVENTS0.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->time.step|447|0|8|||||||||||
TLOGS.EL.EVENTS0.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->note|448|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EL.EVENTS1.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->group|452|0|8|||||||||||
TLOGS.EL.EVENTS1.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->local|453|0|32|||||||||||
TLOGS.EL.EVENTS1.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->time.total_cycle|457|0|32|||||||||||
TLOGS.EL.EVENTS1.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->time.step|461|0|8|||||||||||
TLOGS.EL.EVENTS1.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->note|462|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EL.EVENTS2.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->group|466|0|8|||||||||||
TLOGS.EL.EVENTS2.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->local|467|0|32|||||||||||
TLOGS.EL.EVENTS2.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->time.total_cycle|471|0|32|||||||||||
TLOGS.EL.EVENTS2.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->time.step|475|0|8|||||||||||
TLOGS.EL.EVENTS2.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->note|476|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EL.EVENTS3.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->group|480|0|8|||||||||||
TLOGS.EL.EVENTS3.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->local|481|0|32|||||||||||
TLOGS.EL.EVENTS3.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->time.total_cycle|485|0|32|||||||||||
TLOGS.EL.EVENTS3.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->time.step|489|0|8|||||||||||
TLOGS.EL.EVENTS3.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->note|490|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EH.EVENTS0.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->group|494|0|8|||||||||||
TLOGS.EH.EVENTS0.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->local|495|0|32|||||||||||
TLOGS.EH.EVENTS0.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->time.total_cycle|499|0|32|||||||||||
TLOGS.EH.EVENTS0.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->time.step|503|0|8|||||||||||
TLOGS.EH.EVENTS0.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->note|504|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EH.EVENTS1.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->group|508|0|8|||||||||||
TLOGS.EH.EVENTS1.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->local|509|0|32|||||||||||
TLOGS.EH.EVENTS1.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->time.total_cycle|513|0|32|||||||||||
TLOGS.EH.EVENTS1.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->time.step|517|0|8|||||||||||
TLOGS.EH.EVENTS1.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->note|518|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EH.EVENTS2.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->group|522|0|8|||||||||||
TLOGS.EH.EVENTS2.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->local|523|0|32|||||||||||
TLOGS.EH.EVENTS2.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->time.total_cycle|527|0|32|||||||||||
TLOGS.EH.EVENTS2.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->time.step|531|0|8|||||||||||
TLOGS.EH.EVENTS2.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->note|532|0|32|||||||||ここぐらいはu32でおろす||
TLOGS.EH.EVENTS3.GROUP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->group|536|0|8|||||||||||
TLOGS.EH.EVENTS3.LOCAL|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->local|537|0|32|||||||||||
TLOGS.EH.EVENTS3.TIME.TOTAL_CYCLE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->time.total_cycle|541|0|32|||||||||||
TLOGS.EH.EVENTS3.TIME.STEP|uint8_t|(uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->time.step|545|0|8|||||||||||
TLOGS.EH.EVENTS3.NOTE|uint32_t|(uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->note|546|0|32|||||||||ここぐらいはu32でおろす||
