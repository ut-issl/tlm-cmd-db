# SAMPLE_AOBC_CMD_DB_CMD_DB

## CDH

Name|Code|Params|Param1||Param2||Param3||Param4||Param5||Param6||Danger|Restricted|Desc.|Note
-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-|-

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
Cmd_NOP|0x0|0|||||||||||||||ｿｽ_ｿｽ~ｿｽ[ｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_TMGR_SET_TIME|0x1|1|uint32_t||||||||||||||MOBCｿｽｿｽｿｽｿｽｿｽﾝ抵ｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_TMGR_UPDATE_UNIXTIME|0x2|3|double||uint32_t||uint32_t||||||||||MOBC UNIXTIMEｿｽCｿｽｿｽｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_TMGR_SET_UTL_UNIXTIME_EPOCH|0x3|1|double||||||||||||||UTL_cmdｿｽﾅ用ｿｽｿｽｿｽｿｽunixtimeｿｽﾌ紀ｿｽｿｽｿｽｿｽﾏ更ｿｽｿｽｿｽｿｽ|utl_unixtime_epoch [s]|
Cmd_TMGR_SET_CYCLE_CORRECTION|0x4|1|double||||||||||||||CYCLES_PER_SECｿｽﾌ補正ｿｽ{ｿｽｿｽｿｽｿｽﾏ更ｿｽｿｽｿｽｿｽ, ｿｽｿｽｿｽｿｽｿｽlｿｽｿｽ1.0||
Cmd_TMGR_RESET_CYCLE_CORRECTION|0x5|0|||||||||||||||CYCLES_PER_SECｿｽﾌ補正ｿｽ{ｿｽｿｽｿｽｿｽ1.0ｿｽﾉ擾ｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽ||
Cmd_TMGR_CLEAR_UNIXTIME_INFO|0x6|0|||||||||||||||unixtime_info_ ｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽ||
Cmd_AM_REGISTER_APP|0x7|3|uint32_t||uint32_t||uint32_t||||||||||ｿｽAｿｽvｿｽｿｽｿｽoｿｽ^ｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_AM_INITIALIZE_APP|0x8|1|uint32_t||||||||||||||ｿｽAｿｽvｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_AM_EXECUTE_APP|0x9|1|uint32_t||||||||||||||ｿｽAｿｽvｿｽｿｽｿｽｿｽｿｽsｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_AM_SET_PAGE_FOR_TLM|0xa|1|uint8_t||||||||||||||ｿｽeｿｽｿｽｿｽｿｽｿｽgｿｽｿｽｿｽｿｽｿｽｿｽｿｽpｿｽyｿｽ[ｿｽWｿｽﾔ搾ｿｽｿｽﾝ抵ｿｽ||
Cmd_AM_CLEAR_APP_INFO|0xb|0|||||||||||||o||ｿｽAｿｽvｿｽｿｽｿｽｿｽｿｽsｿｽｿｽｿｽﾔ計ｿｽｿｽｿｽﾌ擾ｿｽｿｽｿｽｿｽｿｽ||
Cmd_MM_SET_MODE_LIST|0xc|2|uint8_t||uint16_t||||||||||||ｿｽｿｽｿｽ[ｿｽhｿｽｿｽ`ｿｽｿｽｿｽXｿｽgｿｽﾝ抵ｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_MM_SET_TRANSITION_TABLE|0xd|3|uint8_t||uint8_t||uint16_t||||||||||ｿｽｿｽｿｽ[ｿｽhｿｽJｿｽﾚ抵ｿｽ`ｿｽeｿｽ[ｿｽuｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_MM_START_TRANSITION|0xe|1|uint8_t||||||||||||||ｿｽｿｽｿｽ[ｿｽhｿｽJｿｽﾚ開ｿｽnｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_MM_FINISH_TRANSITION|0xf|0|||||||||||||||ｿｽｿｽｿｽ[ｿｽhｿｽJｿｽﾚ終ｿｽｿｽｿｽﾊ知ｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_MM_UPDATE_TRANSITION_TABLE_FOR_TLM|0x10|0|||||||||||||||ｿｽｿｽｿｽ[ｿｽhｿｽｿｽTLMｿｽeｿｽ[ｿｽuｿｽｿｽｿｽｿｽｿｽXｿｽV||
Cmd_TDSP_SET_TASK_LIST|0x11|1|uint8_t||||||||||||||ｿｽ^ｿｽXｿｽNｿｽｿｽｿｽXｿｽgｿｽﾝ抵ｿｽRｿｽ}ｿｽｿｽｿｽh||
Cmd_TLCD_CLEAR_ALL_TIMELINE|0x12|1|uint8_t||||||||||||o||ｿｽSTLCｿｽoｿｽ^ｿｽｿｽｿｽｿｽ||
Cmd_TLCD_CLEAR_TIMELINE_AT|0x13|2|uint8_t||uint32_t||||||||||||TIｿｽwｿｽｿｽTLCｿｽoｿｽ^ｿｽｿｽｿｽｿｽ||
Cmd_TLCD_SET_LINE_NO_FOR_TIMELINE_TLM|0x14|1|uint8_t||||||||||||||TLCｿｽｵ一覧ｿｽXｿｽV||
Cmd_TLCD_DEPLOY_BLOCK|0x15|2|uint8_t||uint16_t||||||||||||BLCｿｽWｿｽJ ||
Cmd_TLCD_SET_SOE_FLAG|0x16|2|uint8_t||uint8_t||||||||||||ｿｽﾙ常時ｿｽｿｽｿｽsｿｽｿｽ~ｿｽ@ｿｽ\ｿｽﾝ抵ｿｽ(ｿｽｿｽｿｽCｿｽｿｽｿｽﾔ搾ｿｽ, ｿｽtｿｽｿｽｿｽO)||
Cmd_TLCD_SET_LOUT_FLAG|0x17|2|uint8_t||uint8_t||||||||||||ｿｽｿｽｿｽsｿｽｿｽ~ｿｽ@ｿｽ\ｿｽﾝ抵ｿｽ(ｿｽｿｽｿｽCｿｽｿｽｿｽﾔ搾ｿｽ, ｿｽtｿｽｿｽｿｽO)||
Cmd_TLCD_SET_PAGE_FOR_TLM|0x18|1|uint8_t||||||||||||||ｿｽeｿｽｿｽｿｽｿｽｿｽgｿｽｿｽｿｽｿｽｿｽｿｽｿｽpｿｽyｿｽ[ｿｽWｿｽﾔ搾ｿｽｿｽﾝ抵ｿｽ||
Cmd_TLCD_CLEAR_ERR_LOG|0x19|1|uint8_t||||||||||||||ｿｽﾅ新ｿｽﾌコｿｽ}ｿｽｿｽｿｽhｿｽｿｽｿｽsｿｽﾙ擾ｿｽLｿｽ^ｿｽｿｽｿｽNｿｽｿｽｿｽA||
Cmd_GENERATE_TLM|0x1a|3|uint8_t||uint8_t||uint8_t||||||||||TLMｿｽpｿｽPｿｽbｿｽgｿｽｿｽｿｽｿｽ||

