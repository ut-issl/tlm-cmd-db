# SAMPLE_MOBC_CMD_DB_CMD_DB

## POWER

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## COM

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## MISSION

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## PROP

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## AOCS

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## Thermal

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## Trajectory

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## HILS

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

## C2A_CORE

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
Cmd_NOP|0x0|0||||||||||||||
Cmd_TMGR_SET_TIME|0x1|1|uint32_t|TI||||||||||||
Cmd_TMGR_UPDATE_UNIXTIME|0x2|3|double|unixtime|uint32_t|total_cycle|uint32_t|step||||||||
Cmd_TMGR_SET_UTL_UNIXTIME_EPOCH|0x3|1|double|ult_unixtime_epoch||||||||||||
Cmd_TMGR_SET_CYCLE_CORRECTION|0x4|1|double|cycle_correction||||||||||||
Cmd_TMGR_RESET_CYCLE_CORRECTION|0x5|0||||||||||||||
Cmd_TMGR_CLEAR_UNIXTIME_INFO|0x6|0||||||||||||||
Cmd_AM_REGISTER_APP|0x7|3|uint32_t|app_id|uint32_t|init_ptr|uint32_t|entry_ptr||||||||
Cmd_AM_INITIALIZE_APP|0x8|1|uint32_t|app_id||||||||||||
Cmd_AM_EXECUTE_APP|0x9|1|uint32_t|app_id||||||||||||
Cmd_AM_SET_PAGE_FOR_TLM|0xa|1|uint8_t|||||||||||||
Cmd_AM_CLEAR_APP_INFO|0xb|0|||||||||||||o|
Cmd_MM_SET_MODE_LIST|0xc|2|uint8_t|mode|uint16_t|bc_index||||||||||
Cmd_MM_SET_TRANSITION_TABLE|0xd|3|uint8_t|from_mode|uint8_t|to_mode|uint16_t|bc_index||||||||
Cmd_MM_START_TRANSITION|0xe|1|uint8_t|to_mode||||||||||||
Cmd_MM_FINISH_TRANSITION|0xf|0||||||||||||||
Cmd_MM_UPDATE_TRANSITION_TABLE_FOR_TLM|0x10|0||||||||||||||
Cmd_TDSP_SET_TASK_LIST|0x11|1|uint8_t|bc_index||||||||||||
Cmd_TLCD_CLEAR_ALL_TIMELINE|0x12|1|uint8_t|TLCD_ID|||||||||||o|
Cmd_TLCD_CLEAR_TIMELINE_AT|0x13|2|uint8_t|TLCD_ID|uint32_t|TI||||||||||
Cmd_TLCD_DEPLOY_BLOCK|0x14|2|uint8_t|TLCD_ID|uint16_t|bc_index||||||||||
Cmd_TLCD_CLEAR_ERR_LOG|0x15|1|uint8_t|||||||||||||
Cmd_TLCD_SET_SOE_FLAG|0x16|2|uint8_t|TLCD_ID|uint8_t|||||||||||
Cmd_TLCD_SET_LOUT_FLAG|0x17|2|uint8_t|TLCD_ID|uint8_t|||||||||||
Cmd_TLCD_SET_ID_FOR_TLM|0x18|1|uint8_t|TLCD_ID||||||||||||
Cmd_TLCD_SET_PAGE_FOR_TLM|0x19|1|uint8_t|page_no||||||||||||
Cmd_GENERATE_TLM|0x1a|3|uint8_t|category|uint8_t|TLM_ID|uint8_t|送出回数||||||||
Cmd_BCT_CLEAR_BLOCK|0x1b|1|uint16_t|bc_index||||||||||||
Cmd_BCT_SET_BLOCK_POSITION|0x1c|2|uint16_t|bc_index|uint8_t|cmd_index||||||||||
Cmd_BCT_COPY_BCT|0x1d|2|uint16_t|dst_bc_index|uint16_t|src_bc_index||||||||||
Cmd_BCT_OVERWRITE_CMD|0x1e|5|uint16_t|CMD_CODE|uint32_t|TI|uint16_t|pos.block|uint8_t|pos.cmd|raw|cmd_param (big endian)|||o|
Cmd_BCT_FILL_NOP|0x1f|1|uint8_t|||||||||||||
Cmd_BCE_ACTIVATE_BLOCK|0x20|0||||||||||||||
Cmd_BCE_ACTIVATE_BLOCK_BY_ID|0x21|1|uint16_t|bc_index||||||||||||
Cmd_BCE_INACTIVATE_BLOCK_BY_ID|0x22|1|uint16_t|bc_index||||||||||||
Cmd_BCE_ROTATE_BLOCK|0x23|1|uint16_t|bc_index||||||||||||
Cmd_BCE_COMBINE_BLOCK|0x24|1|uint16_t|bc_index||||||||||||
Cmd_BCE_TIMELIMIT_COMBINE_BLOCK|0x25|2|uint16_t|bc_index|uint8_t|limit_step||||||||||
Cmd_BCE_RESET_ROTATOR_INFO|0x26|0|||||||||||||o|
Cmd_BCE_RESET_COMBINER_INFO|0x27|0|||||||||||||o|
Cmd_BCE_SET_ROTATE_INTERVAL|0x28|2|uint16_t||uint16_t|||||||||||
Cmd_GSCD_CLEAR_ERR_LOG|0x29|0||||||||||||||
Cmd_RTCD_CLEAR_ALL_REALTIME|0x2a|0|||||||||||||o|
Cmd_RTCD_CLEAR_ERR_LOG|0x2b|0||||||||||||||
Cmd_MEM_SET_REGION|0x2c|2|uint32_t|始点アドレス|uint32_t|終点アドレス||||||||||
Cmd_MEM_DUMP_REGION_SEQ||2|uint8_t|category|uint8_t|送出回数||||||||||
Cmd_MEM_DUMP_REGION_RND||3|uint8_t|category|uint8_t|送出回数|uint16_t|ダンプ位置||||||||
Cmd_MEM_DUMP_SINGLE||3|uint8_t|category|uint8_t|送出回数|uint32_t|ダンプ位置||||||||
Cmd_MEM_LOAD|0x30|2|uint32_t|開始アドレス|raw|HEXBINARY||||||||||
Cmd_MEM_SET_DESTINATION|0x31|1|uint32_t|コピー先アドレス||||||||||||
Cmd_MEM_COPY_REGION_SEQ|0x32|1|uint32_t|コピー幅||||||||||||
Cmd_AL_ADD_ANOMALY|0x33|2|uint32_t|group|uint32_t|local||||||||||
Cmd_AL_CLEAR_LIST|0x34|0||||||||||||||
Cmd_AL_SET_PAGE_FOR_TLM|0x35|1|uint8_t|page no||||||||||||
Cmd_AL_INIT_LOGGING_ENA_FLAG|0x36|0||||||||||||||
Cmd_AL_ENABLE_LOGGING|0x37|1|uint32_t|group||||||||||||
Cmd_AL_DISABLE_LOGGING|0x38|1|uint32_t|group||||||||||||
Cmd_AL_SET_THRES_OF_NEARLY_FULL|0x39|1|uint16_t|||||||||||||
Cmd_AH_REGISTER_RULE|0x3a|6|uint8_t|id|uint8_t|group|uint8_t|local|uint8_t|cond|uint8_t|threshold|uint16_t|bc_index||
Cmd_AH_ACTIVATE_RULE|0x3b|1|uint8_t|id||||||||||||
Cmd_AH_INACTIVATE_RULE|0x3c|1|uint8_t|id||||||||||||
Cmd_AH_CLEAR_LOG|0x3d|0||||||||||||||
Cmd_AH_SET_PAGE_FOR_TLM|0x3e|1|uint8_t|page no||||||||||||
Cmd_AHRES_LOG_CLEAR|0x3f|0||||||||||||||
Cmd_AHRES_LOG_SET_PAGE_FOR_TLM|0x40|1|uint8_t|page no||||||||||||
Cmd_EL_INIT|0x41|0||||||||||||||
Cmd_EL_CLEAR_LOG_ALL|0x42|0||||||||||||||
Cmd_EL_CLEAR_LOG_BY_ERR_LEVEL|0x43|1|uint8_t|err_level||||||||||||
Cmd_EL_CLEAR_STATISTICS|0x44|0||||||||||||||
Cmd_EL_CLEAR_TLOG|0x45|1|uint8_t|err_level||||||||||||
Cmd_EL_CLEAR_CLOG|0x46|1|uint8_t|err_level||||||||||||
Cmd_EL_RECORD_EVENT|0x47|4|uint32_t|group|uint32_t|local|uint8_t|err_level|uint32_t|note||||||
Cmd_EL_TLOG_SET_PAGE_FOR_TLM|0x48|2|uint8_t|page_no|uint8_t|err_level||||||||||
Cmd_EL_CLOG_SET_PAGE_FOR_TLM|0x49|2|uint8_t|page_no|uint8_t|err_level||||||||||
Cmd_EL_INIT_LOGGING_SETTINGS|0x4a|0||||||||||||||
Cmd_EL_ENABLE_LOGGING|0x4b|1|uint32_t|group||||||||||||
Cmd_EL_DISABLE_LOGGING|0x4c|1|uint32_t|group||||||||||||
Cmd_EL_ENABLE_LOGGING_ALL|0x4d|0||||||||||||||
Cmd_EL_DISABLE_LOGGING_ALL|0x4e|0||||||||||||||
Cmd_EL_ENABLE_TLOG_OVERWRITE|0x4f|1|uint8_t|err_level||||||||||||
Cmd_EL_DISABLE_TLOG_OVERWRITE|0x50|1|uint8_t|err_level||||||||||||
Cmd_EL_ENABLE_TLOG_OVERWRITE_ALL|0x51|0||||||||||||||
Cmd_EL_DISABLE_TLOG_OVERWRITE_ALL|0x52|0||||||||||||||
Cmd_EH_INIT|0x53|0||||||||||||||
Cmd_EH_CLEAR_ALL_RULE|0x54|0||||||||||||||
Cmd_EH_LOAD_DEFAULT_RULE|0x55|0||||||||||||||
Cmd_EH_SET_REGISTER_RULE_EVENT_PARAM|0x56|6|uint16_t|rule id|uint32_t|event group|uint32_t|event local|uint8_t|event err level|uint8_t|should_match_err_level|uint16_t|deploy bc index||
Cmd_EH_SET_REGISTER_RULE_CONDITION_PARAM|0x57|4|uint8_t|condition type|uint16_t|count_threshold|uint32_t|time_threshold [ms]|uint8_t|is_active||||||
Cmd_EH_REGISTER_RULE|0x58|0||||||||||||||
Cmd_EH_DELETE_RULE|0x59|1|uint16_t|rule id||||||||||||
Cmd_EH_INIT_RULE|0x5a|1|uint16_t|rule id||||||||||||
Cmd_EH_INIT_RULE_FOR_MULTI_LEVEL|0x5b|1|uint16_t|rule id||||||||||||
Cmd_EH_ACTIVATE_RULE|0x5c|1|uint16_t|rule id||||||||||||
Cmd_EH_INACTIVATE_RULE|0x5d|1|uint16_t|rule id||||||||||||
Cmd_EH_ACTIVATE_RULE_FOR_MULTI_LEVEL|0x5e|1|uint16_t|rule id||||||||||||
Cmd_EH_INACTIVATE_RULE_FOR_MULTI_LEVEL|0x5f|1|uint16_t|rule id||||||||||||
Cmd_EH_SET_RULE_COUNTER|0x60|2|uint16_t|rule id|uint16_t|counter||||||||||
Cmd_EH_CLEAR_RULE_COUNTER|0x61|1|uint16_t|rule id||||||||||||
Cmd_EH_CLEAR_RULE_COUNTER_BY_EVENT|0x62|3|uint32_t|group|uint32_t|local|uint8_t|err_level||||||||
Cmd_EH_CLEAR_LOG|0x63|0||||||||||||||
Cmd_EH_SET_MAX_RESPONSE_NUM|0x64|1|uint8_t|max_response_num||||||||||||
Cmd_EH_SET_MAX_CHECK_EVENT_NUM|0x65|1|uint16_t|max_check_event_num||||||||||||
Cmd_EH_SET_MAX_MULTI_LEVEL_NUM|0x66|1|uint8_t|max_multi_level_num||||||||||||
Cmd_EH_SET_PAGE_OF_RULE_TABLE_FOR_TLM|0x67|1|uint8_t|page_no||||||||||||
Cmd_EH_SET_PAGE_OF_RULE_SORTED_IDX_FOR_TLM|0x68|1|uint8_t|page_no||||||||||||
Cmd_EH_SET_PAGE_OF_LOG_TABLE_FOR_TLM|0x69|1|uint8_t|page_no||||||||||||
Cmd_EH_SET_TARGET_ID_OF_RULE_TABLE_FOR_TLM|0x6a|1|uint16_t|rule id||||||||||||
Cmd_EH_MATCH_EVENT_COUNTER_TO_EL|0x6b|0||||||||||||||
Cmd_EVENT_UTIL_ENABLE_EH_EXEC|0x6c|0||||||||||||||
Cmd_EVENT_UTIL_DISABLE_EH_EXEC|0x6d|0||||||||||||||
Cmd_EVENT_UTIL_EXEC_EH|0x6e|0||||||||||||||
Cmd_TF_INIT|0x6f|0||||||||||||||
Cmd_CA_INIT|0x70|0||||||||||||||
Cmd_TF_REGISTER_TLM|0x71|2|uint8_t|index|uint32_t|tlm_func||||||||||
Cmd_CA_REGISTER_CMD|0x72|3|uint16_t|index|uint32_t|cmd_func|raw|param_info||||||||
Cmd_TF_SET_PAGE_FOR_TLM|0x73|1|uint8_t|page_no||||||||||||
Cmd_CA_SET_PAGE_FOR_TLM|0x74|1|uint8_t|page_no||||||||||||
Cmd_TLM_MGR_INIT|0x75|0||||||||||||||
Cmd_TLM_MGR_INIT_MASTER_BC|0x76|0||||||||||||||
Cmd_TLM_MGR_CLEAR_HK_TLM|0x77|0||||||||||||||
Cmd_TLM_MGR_CLEAR_SYSTEM_TLM|0x78|0||||||||||||||
Cmd_TLM_MGR_CLEAR_USER_TLM|0x79|0||||||||||||||
Cmd_TLM_MGR_START_TLM|0x7a|0||||||||||||||
Cmd_TLM_MGR_STOP_TLM|0x7b|0||||||||||||||
Cmd_TLM_MGR_CLEAR_TLM_TL|0x7c|0||||||||||||||
Cmd_TLM_MGR_REGISTER_HK_TLM|0x7d|3|uint8_t|category|uint8_t|TLM_ID|uint8_t|送出回数||||||||
Cmd_TLM_MGR_REGISTER_SYSTEM_TLM|0x7e|3|uint8_t|category|uint8_t|TLM_ID|uint8_t|送出回数||||||||
Cmd_TLM_MGR_REGISTER_HIGH_FREQ_TLM|0x7f|3|uint8_t|category|uint8_t|TLM_ID|uint8_t|送出回数||||||||
Cmd_TLM_MGR_REGISTER_LOW_FREQ_TLM|0x80|3|uint8_t|category|uint8_t|TLM_ID|uint8_t|送出回数||||||||
Cmd_DCU_ABORT_CMD|0x81|1|uint16_t|Cmd ID||||||||||||
Cmd_DCU_DOWN_ABORT_FLAG|0x82|1|uint16_t|Cmd ID||||||||||||
Cmd_DCU_CLEAR_LOG|0x83|0||||||||||||||

## CDH

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
Cmd_DI_GS_CCSDS_TX_START|0x100|0||||||||||||||
Cmd_DI_GS_CCSDS_TX_STOP|0x101|0|||||||||||||o|
Cmd_DI_GS_DRIVER_RESET|0x102|0||||||||||||||
Cmd_DI_GS_SET_MS_FLUSH_INTERVAL|0x103|1|uint32_t|排出間隔||||||||||||
Cmd_DI_GS_SET_RP_FLUSH_INTERVAL|0x104|1|uint32_t|排出間隔||||||||||||
Cmd_DI_GS_SET_FARM_PW|0x105|1|uint8_t|positive_window_width||||||||||||
Cmd_DI_GS_SET_INFO|0x106|1|uint8_t|TLM選択||||||||||||
Cmd_DI_GS_CCSDS_GET_BUFFER|0x107|0||||||||||||||
Cmd_DI_GS_CCSDS_SET_RATE|0x108|1|uint8_t|bps セットパラメータ|||||||||||o|
Cmd_WDT_INIT|0x109|0||||||||||||||
Cmd_WDT_ENABLE|0x10a|0||||||||||||||
Cmd_WDT_DISABLE|0x10b|0||||||||||||||
Cmd_WDT_STOP_CLEAR|0x10c|0|||||||||||||o|
Cmd_WDT_START_CLEAR|0x10d|0||||||||||||||
Cmd_UART_TEST_INIT_DI|0x10e|0||||||||||||||
Cmd_UART_TEST_UPDATE|0x10f|0||||||||||||||
Cmd_UART_TEST_SEND_TEST|0x110|1|uint8_t|id||||||||||||

## Other

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
Cmd_UTIL_CMD_ADD|0x3e0|6|uint8_t||uint32_t||uint32_t||uint32_t||uint32_t||uint32_t|||
Cmd_UTIL_CMD_SEND|0x3e1|1|uint8_t|||||||||||||
Cmd_UTIL_CMD_RESET|0x3e2|0||||||||||||||
Cmd_UTIL_COUNTER_INCREMENT|0x3e3|1|uint8_t|||||||||||||
Cmd_UTIL_COUNTER_RESET|0x3e4|1|uint8_t|||||||||||||
Cmd_UTIL_COUNTER_SET_PARAM|0x3e5|3|uint8_t||uint32_t||uint8_t|||||||||

## NonOrder

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-
Cmd_OBC_CHECK_SIB_VERSION|0x3e6|0||||||||||||||

