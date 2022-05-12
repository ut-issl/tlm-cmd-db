#pragma section REPRO
/**
 * @file
 * @brief  テレメトリ定義
 * @note   このコードは自動生成されています！
 */
# include "../../src_core/TlmCmd/telemetry_frame.h"
# include "telemetry_definitions.h"
# include "telemetry_source.h"

static TF_TLM_FUNC_ACK Tlm_MOBC_(uint8_t* packet, uint16_t* len, uint16_t max_len);
static TF_TLM_FUNC_ACK Tlm_AOBC_AOBC_(uint8_t* packet, uint16_t* len, uint16_t max_len);
static TF_TLM_FUNC_ACK Tlm_AOBC_HK_(uint8_t* packet, uint16_t* len, uint16_t max_len);
static TF_TLM_FUNC_ACK Tlm_HK_(uint8_t* packet, uint16_t* len, uint16_t max_len);

void TF_load_tlm_table(TF_TlmInfo tlm_table[TF_MAX_TLMS])
{
  tlm_table[Tlm_CODE_MOBC].tlm_func = Tlm_MOBC_;
  tlm_table[Tlm_CODE_AOBC_AOBC].tlm_func = Tlm_AOBC_AOBC_;
  tlm_table[Tlm_CODE_AOBC_HK].tlm_func = Tlm_AOBC_HK_;
  tlm_table[Tlm_CODE_HK].tlm_func = Tlm_HK_;
}

static TF_TLM_FUNC_ACK Tlm_MOBC_(uint8_t* packet, uint16_t* len, uint16_t max_len)
{
  if (322 > max_len) return TF_TLM_FUNC_ACK_TOO_SHORT_LEN;

# ifndef BUILD_SETTINGS_FAST_BUILD
  TF_copy_u32(&packet[26], (uint32_t)(TMGR_get_master_clock().mode_cycle));
  TF_copy_double(&packet[30], TMGR_get_utl_unixtime_epoch());
  TF_copy_double(&packet[38], (double)(time_manager->unixtime_info_.cycle_correction));
  TF_copy_u8(&packet[46], (uint8_t)(mode_manager->stat));
  TF_copy_u8(&packet[47], (uint8_t)(mode_manager->current_id));
  TF_copy_u8(&packet[48], (uint8_t)(mode_manager->previous_id));
  TF_copy_u8(&packet[49], (uint8_t)(TDSP_info->task_list_id));
  TF_copy_u32(&packet[50], (uint32_t)(TDSP_info->tskd.prev_err.time.total_cycle));
  TF_copy_u8(&packet[54], (uint8_t)(TDSP_info->tskd.prev_err.time.step));
  TF_copy_u16(&packet[55], (uint16_t)(TDSP_info->tskd.prev_err.code));
  TF_copy_i32(&packet[57], (int32_t)(TDSP_info->tskd.prev_err.sts));
  TF_copy_i32(&packet[61], (int32_t)gs_driver->latest_info->rx.ret_from_if_rx);
  TF_copy_u8(&packet[65], (uint8_t)gs_driver->latest_info->rx.rec_status);
  TF_copy_u32(&packet[66], (uint32_t)gs_driver->latest_info->rx.last_rec_time);
  TF_copy_u8(&packet[70], (uint8_t)gs_validate_info->positive_window_width);
  TF_copy_u8(&packet[71], (uint8_t)gs_driver->latest_info->rx.cmd_ack);
  TF_copy_u8(&packet[72], (uint8_t)gs_driver->tlm_tx_port_type);
  TF_copy_u32(&packet[73], PL_count_executed_nodes(&PH_gs_cmd_list));
  TF_copy_u32(&packet[77], (uint32_t)(gs_command_dispatcher->prev.time.total_cycle));
  TF_copy_u16(&packet[81], (uint16_t)(gs_command_dispatcher->prev.code));
  TF_copy_i32(&packet[83], (int32_t)(gs_command_dispatcher->prev.sts));
  TF_copy_u32(&packet[87], (uint32_t)(gs_command_dispatcher->prev_err.time.total_cycle));
  TF_copy_u16(&packet[91], (uint16_t)(gs_command_dispatcher->prev_err.code));
  TF_copy_i32(&packet[93], (int32_t)(gs_command_dispatcher->prev_err.sts));
  TF_copy_u32(&packet[97], (uint32_t)(gs_command_dispatcher->error_counter));
  TF_copy_u32(&packet[101], PL_count_executed_nodes(&PH_rt_cmd_list));
  TF_copy_u32(&packet[105], (uint32_t)(realtime_command_dispatcher->prev.time.total_cycle));
  TF_copy_u16(&packet[109], (uint16_t)(realtime_command_dispatcher->prev.code));
  TF_copy_i32(&packet[111], (int32_t)(realtime_command_dispatcher->prev.sts));
  TF_copy_u32(&packet[115], (uint32_t)(realtime_command_dispatcher->prev_err.time.total_cycle));
  TF_copy_u16(&packet[119], (uint16_t)(realtime_command_dispatcher->prev_err.code));
  TF_copy_i32(&packet[121], (int32_t)(realtime_command_dispatcher->prev_err.sts));
  TF_copy_u32(&packet[125], (uint32_t)(realtime_command_dispatcher->error_counter));
  TF_copy_u32(&packet[129], PL_count_executed_nodes(&PH_tl_cmd_list[TLCD_ID_FROM_GS]));
  TF_copy_u8(&packet[133], (uint8_t)(PL_count_active_nodes(&PH_tl_cmd_list[TLCD_ID_FROM_GS])));
  TF_copy_u32(&packet[134], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].prev.time.total_cycle));
  TF_copy_u16(&packet[138], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].prev.code));
  TF_copy_i32(&packet[140], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].prev.sts));
  TF_copy_u32(&packet[144], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].prev_err.time.total_cycle));
  TF_copy_u16(&packet[148], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].prev_err.code));
  TF_copy_i32(&packet[150], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].prev_err.sts));
  TF_copy_u32(&packet[154], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].error_counter));
  TF_copy_u8(&packet[158], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].stop_on_error));
  TF_copy_u8(&packet[159], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS].lockout));
  TF_copy_u32(&packet[160], (PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_FROM_GS])) ? 0 : (uint32_t)CCP_get_ti((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_FROM_GS]))->packet))));
  TF_copy_u16(&packet[164], (uint16_t)(PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_FROM_GS])) ? 0 : CCP_get_id((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_FROM_GS]))->packet))));
  TF_copy_u32(&packet[166], PL_count_executed_nodes(&PH_tl_cmd_list[TLCD_ID_DEPLOY_BC]));
  TF_copy_u8(&packet[170], (uint8_t)(PL_count_active_nodes(&PH_tl_cmd_list[TLCD_ID_DEPLOY_BC])));
  TF_copy_u32(&packet[171], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].prev.time.total_cycle));
  TF_copy_u16(&packet[175], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].prev.code));
  TF_copy_i32(&packet[177], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].prev.sts));
  TF_copy_u32(&packet[181], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].prev_err.time.total_cycle));
  TF_copy_u16(&packet[185], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].prev_err.code));
  TF_copy_i32(&packet[187], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].prev_err.sts));
  TF_copy_u32(&packet[191], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].error_counter));
  TF_copy_u8(&packet[195], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].stop_on_error));
  TF_copy_u8(&packet[196], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_BC].lockout));
  TF_copy_u32(&packet[197], (PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_BC])) ? 0 : (uint32_t)CCP_get_ti((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_BC]))->packet))));
  TF_copy_u16(&packet[201], (uint16_t)(PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_BC])) ? 0 : CCP_get_id((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_BC]))->packet))));
  TF_copy_u32(&packet[203], PL_count_executed_nodes(&PH_tl_cmd_list[TLCD_ID_DEPLOY_TLM]));
  TF_copy_u8(&packet[207], (uint8_t)(PL_count_active_nodes(&PH_tl_cmd_list[TLCD_ID_DEPLOY_TLM])));
  TF_copy_u32(&packet[208], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].prev.time.total_cycle));
  TF_copy_u16(&packet[212], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].prev.code));
  TF_copy_i32(&packet[214], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].prev.sts));
  TF_copy_u32(&packet[218], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].prev_err.time.total_cycle));
  TF_copy_u16(&packet[222], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].prev_err.code));
  TF_copy_i32(&packet[224], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].prev_err.sts));
  TF_copy_u32(&packet[228], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].error_counter));
  TF_copy_u8(&packet[232], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].stop_on_error));
  TF_copy_u8(&packet[233], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_DEPLOY_TLM].lockout));
  TF_copy_u32(&packet[234], (PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_TLM])) ? 0 : (uint32_t)CCP_get_ti((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_TLM]))->packet))));
  TF_copy_u16(&packet[238], (uint16_t)(PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_TLM])) ? 0 : CCP_get_id((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_DEPLOY_TLM]))->packet))));
  TF_copy_u32(&packet[240], PL_count_executed_nodes(&PH_tl_cmd_list[TLCD_ID_FROM_GS_FOR_MISSION]));
  TF_copy_u8(&packet[244], (uint8_t)(PL_count_active_nodes(&PH_tl_cmd_list[TLCD_ID_FROM_GS_FOR_MISSION])));
  TF_copy_u32(&packet[245], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].prev.time.total_cycle));
  TF_copy_u16(&packet[249], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].prev.code));
  TF_copy_i32(&packet[251], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].prev.sts));
  TF_copy_u32(&packet[255], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].prev_err.time.total_cycle));
  TF_copy_u16(&packet[259], (uint16_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].prev_err.code));
  TF_copy_i32(&packet[261], (int32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].prev_err.sts));
  TF_copy_u32(&packet[265], (uint32_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].error_counter));
  TF_copy_u8(&packet[269], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].stop_on_error));
  TF_copy_u8(&packet[270], (uint8_t)(timeline_command_dispatcher->dispatcher[TLCD_ID_FROM_GS_FOR_MISSION].lockout));
  TF_copy_u32(&packet[271], (PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_FROM_GS_FOR_MISSION])) ? 0 : (uint32_t)CCP_get_ti((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_FROM_GS_FOR_MISSION]))->packet))));
  TF_copy_u16(&packet[275], (uint16_t)(PL_is_empty(&(PH_tl_cmd_list[TLCD_ID_FROM_GS_FOR_MISSION])) ? 0 : CCP_get_id((const CommonCmdPacket*)(PL_get_head(&(PH_tl_cmd_list[TLCD_ID_FROM_GS_FOR_MISSION]))->packet))));
  TF_copy_u8(&packet[277], (uint8_t)(block_command_table->pos.block));
  TF_copy_u8(&packet[278], (uint8_t)(block_command_table->pos.cmd));
  TF_copy_u32(&packet[279], ((block_command_table->pos.cmd == 0) ? 0 : (uint32_t)BCT_get_ti(block_command_table->pos.block, (uint8_t)(block_command_table->pos.cmd-1))));
  TF_copy_u16(&packet[283], (uint16_t)((block_command_table->pos.cmd == 0) ? 0 : BCT_get_id(block_command_table->pos.block, (uint8_t)(block_command_table->pos.cmd-1))));
  TF_copy_u8(&packet[285], gs_driver->ccsds_info.buffer_num);
  TF_copy_u32(&packet[286], (uint32_t)(DI_GS_ms_tlm_packet_handler->tc_packet_to_m_pdu.flush_interval));
  TF_copy_u32(&packet[290], (uint32_t)(DI_GS_rp_tlm_packet_handler->tc_packet_to_m_pdu.flush_interval));
  TF_copy_u32(&packet[294], PL_count_executed_nodes(&PH_ms_tlm_list));
  TF_copy_u8(&packet[298], (uint8_t)(PL_count_active_nodes(&PH_ms_tlm_list)));
  TF_copy_u32(&packet[299], PL_count_executed_nodes(&PH_st_tlm_list));
  TF_copy_u8(&packet[303], (uint8_t)(PL_count_active_nodes(&PH_st_tlm_list)));
  TF_copy_u32(&packet[304], PL_count_executed_nodes(&PH_rp_tlm_list));
  TF_copy_u8(&packet[308], (uint8_t)(PL_count_active_nodes(&PH_rp_tlm_list)));
  TF_copy_u32(&packet[309], (uint32_t)gs_driver->latest_info->tx.send_cycle);
  TF_copy_u32(&packet[313], gs_driver->driver_ccsds.ccsds_config.bitrate);
  TF_copy_u8(&packet[317], (uint8_t)gs_driver->latest_info->tx.vcid);
  TF_copy_u32(&packet[318], gs_driver->latest_info->tx.vcdu_counter);
# endif

  *len = 322;
  return TF_TLM_FUNC_ACK_SUCCESS;
}

static TF_TLM_FUNC_ACK Tlm_HK_(uint8_t* packet, uint16_t* len, uint16_t max_len)
{
  if (550 > max_len) return TF_TLM_FUNC_ACK_TOO_SHORT_LEN;

# ifndef BUILD_SETTINGS_FAST_BUILD
  TF_copy_u8(&packet[26], (uint8_t)(gs_driver->latest_info->rx.cmd_ack));
  TF_copy_u8(&packet[27], (uint8_t)(((uint8_t)(mode_manager->stat) << 7 & 0x80) | ((uint8_t)(mode_manager->previous_id) << 0 & 0x7f)));
  TF_copy_u16(&packet[28], (uint16_t)BCT_get_id(block_command_table->pos.block, 0));
  TF_copy_u32(&packet[30], (uint32_t)BCT_get_ti(block_command_table->pos.block, 0));
  TF_copy_u16(&packet[34], (uint16_t)BCT_get_id(block_command_table->pos.block, 1));
  TF_copy_u32(&packet[36], (uint32_t)BCT_get_ti(block_command_table->pos.block, 1));
  TF_copy_u16(&packet[40], (uint16_t)BCT_get_id(block_command_table->pos.block, 2));
  TF_copy_u32(&packet[42], (uint32_t)BCT_get_ti(block_command_table->pos.block, 2));
  TF_copy_u16(&packet[46], (uint16_t)BCT_get_id(block_command_table->pos.block, 3));
  TF_copy_u32(&packet[48], (uint32_t)BCT_get_ti(block_command_table->pos.block, 3));
  TF_copy_u16(&packet[52], (uint16_t)BCT_get_id(block_command_table->pos.block, 4));
  TF_copy_u32(&packet[54], (uint32_t)BCT_get_ti(block_command_table->pos.block, 4));
  TF_copy_u16(&packet[58], (uint16_t)BCT_get_id(block_command_table->pos.block, 5));
  TF_copy_u32(&packet[60], (uint32_t)BCT_get_ti(block_command_table->pos.block, 5));
  TF_copy_u16(&packet[64], (uint16_t)BCT_get_id(block_command_table->pos.block, 6));
  TF_copy_u32(&packet[66], (uint32_t)BCT_get_ti(block_command_table->pos.block, 6));
  TF_copy_u16(&packet[70], (uint16_t)BCT_get_id(block_command_table->pos.block, 7));
  TF_copy_u32(&packet[72], (uint32_t)BCT_get_ti(block_command_table->pos.block, 7));
  TF_copy_u16(&packet[76], (uint16_t)BCT_get_id(block_command_table->pos.block, 8));
  TF_copy_u32(&packet[78], (uint32_t)BCT_get_ti(block_command_table->pos.block, 8));
  TF_copy_u16(&packet[82], (uint16_t)BCT_get_id(block_command_table->pos.block, 9));
  TF_copy_u32(&packet[84], (uint32_t)BCT_get_ti(block_command_table->pos.block, 9));
  TF_copy_u16(&packet[88], (uint16_t)BCT_get_id(block_command_table->pos.block, 10));
  TF_copy_u32(&packet[90], (uint32_t)BCT_get_ti(block_command_table->pos.block, 10));
  TF_copy_u32(&packet[94], event_handler->el_event_counter.counters[EL_ERROR_LEVEL_HIGH]);
  TF_copy_u32(&packet[98], event_handler->el_event_counter.counters[EL_ERROR_LEVEL_MIDDLE]);
  TF_copy_u32(&packet[102], event_handler->el_event_counter.counters[EL_ERROR_LEVEL_LOW]);
  TF_copy_u32(&packet[106], event_handler->el_event_counter.counters[EL_ERROR_LEVEL_EL]);
  TF_copy_u32(&packet[110], event_handler->el_event_counter.counters[EL_ERROR_LEVEL_EH]);
  TF_copy_u32(&packet[114], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].initializer));
  TF_copy_u32(&packet[118], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].entry_point));
  TF_copy_u8(&packet[122], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].init_duration));
  TF_copy_u8(&packet[123], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)].prev));
  TF_copy_u32(&packet[124], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].initializer));
  TF_copy_u32(&packet[128], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].entry_point));
  TF_copy_u8(&packet[132], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+0].init_duration));
  TF_copy_u32(&packet[133], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].initializer));
  TF_copy_u32(&packet[137], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].entry_point));
  TF_copy_u8(&packet[141], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+1].init_duration));
  TF_copy_u32(&packet[142], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].initializer));
  TF_copy_u32(&packet[146], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].entry_point));
  TF_copy_u8(&packet[150], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+2].init_duration));
  TF_copy_u32(&packet[151], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+3].initializer));
  TF_copy_u32(&packet[155], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+3].entry_point));
  TF_copy_u8(&packet[159], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+3].init_duration));
  TF_copy_u32(&packet[160], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+4].initializer));
  TF_copy_u32(&packet[164], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+4].entry_point));
  TF_copy_u8(&packet[168], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+4].init_duration));
  TF_copy_u32(&packet[169], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+5].initializer));
  TF_copy_u32(&packet[173], (uint32_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+5].entry_point));
  TF_copy_u8(&packet[177], (uint8_t)(app_manager->ais[(AM_TLM_PAGE_SIZE*app_manager->page_no)+5].init_duration));
  TF_copy_u16(&packet[178], (uint16_t)BCT_get_id(block_command_table->pos.block, 0));
  TF_copy_u8(&packet[180], BCT_get_param_head(block_command_table->pos.block, 0)[0]);
  TF_copy_u8(&packet[181], BCT_get_param_head(block_command_table->pos.block, 0)[1]);
  TF_copy_u8(&packet[182], BCT_get_param_head(block_command_table->pos.block, 0)[2]);
  TF_copy_u8(&packet[183], BCT_get_param_head(block_command_table->pos.block, 0)[3]);
  TF_copy_u8(&packet[184], BCT_get_param_head(block_command_table->pos.block, 0)[4]);
  TF_copy_u8(&packet[185], BCT_get_param_head(block_command_table->pos.block, 0)[5]);
  TF_copy_u16(&packet[186], (uint16_t)BCT_get_id(block_command_table->pos.block, 1));
  TF_copy_u8(&packet[188], BCT_get_param_head(block_command_table->pos.block, 1)[0]);
  TF_copy_u8(&packet[189], BCT_get_param_head(block_command_table->pos.block, 1)[1]);
  TF_copy_u8(&packet[190], BCT_get_param_head(block_command_table->pos.block, 1)[2]);
  TF_copy_u8(&packet[191], BCT_get_param_head(block_command_table->pos.block, 1)[3]);
  TF_copy_u8(&packet[192], BCT_get_param_head(block_command_table->pos.block, 1)[4]);
  TF_copy_u8(&packet[193], BCT_get_param_head(block_command_table->pos.block, 1)[5]);
  TF_copy_u16(&packet[194], (uint16_t)BCT_get_id(block_command_table->pos.block, 2));
  TF_copy_u8(&packet[196], BCT_get_param_head(block_command_table->pos.block, 2)[0]);
  TF_copy_u8(&packet[197], BCT_get_param_head(block_command_table->pos.block, 2)[1]);
  TF_copy_u8(&packet[198], BCT_get_param_head(block_command_table->pos.block, 2)[2]);
  TF_copy_u8(&packet[199], BCT_get_param_head(block_command_table->pos.block, 2)[3]);
  TF_copy_u8(&packet[200], BCT_get_param_head(block_command_table->pos.block, 2)[4]);
  TF_copy_u8(&packet[201], BCT_get_param_head(block_command_table->pos.block, 2)[5]);
  TF_copy_u8(&packet[202], (uint8_t)rules[0 + offset].settings.event.group);
  TF_copy_u32(&packet[203], (uint32_t)rules[0 + offset].settings.event.local);
  TF_copy_u8(&packet[207], (uint8_t)(((uint8_t)rules[0 + offset].settings.event.err_level << 5 & 0xe0) | ((uint8_t)rules[0 + offset].settings.should_match_err_level << 4 & 0x10) | ((uint8_t)rules[0 + offset].settings.is_active << 3 & 0x8) | ((uint8_t)rules[0 + offset].settings.condition.type << 0 & 0x7)));
  TF_copy_u8(&packet[208], (uint8_t)rules[1 + offset].settings.event.group);
  TF_copy_u32(&packet[209], (uint32_t)rules[1 + offset].settings.event.local);
  TF_copy_u8(&packet[213], (uint8_t)(((uint8_t)rules[1 + offset].settings.event.err_level << 5 & 0xe0) | ((uint8_t)rules[1 + offset].settings.should_match_err_level << 4 & 0x10) | ((uint8_t)rules[1 + offset].settings.is_active << 3 & 0x8) | ((uint8_t)rules[1 + offset].settings.condition.type << 0 & 0x7)));
  TF_copy_u8(&packet[214], (uint8_t)rules[2 + offset].settings.event.group);
  TF_copy_u32(&packet[215], (uint32_t)rules[2 + offset].settings.event.local);
  TF_copy_u8(&packet[219], (uint8_t)(((uint8_t)rules[2 + offset].settings.event.err_level << 5 & 0xe0) | ((uint8_t)rules[2 + offset].settings.should_match_err_level << 4 & 0x10) | ((uint8_t)rules[2 + offset].settings.is_active << 3 & 0x8) | ((uint8_t)rules[2 + offset].settings.condition.type << 0 & 0x7)));
  TF_copy_u8(&packet[220], (uint8_t)rules[3 + offset].settings.event.group);
  TF_copy_u32(&packet[221], (uint32_t)rules[3 + offset].settings.event.local);
  TF_copy_u8(&packet[225], (uint8_t)(((uint8_t)rules[3 + offset].settings.event.err_level << 5 & 0xe0) | ((uint8_t)rules[3 + offset].settings.should_match_err_level << 4 & 0x10) | ((uint8_t)rules[3 + offset].settings.is_active << 3 & 0x8) | ((uint8_t)rules[3 + offset].settings.condition.type << 0 & 0x7)));
  TF_copy_u8(&packet[226], (uint8_t)rules[4 + offset].settings.event.group);
  TF_copy_u32(&packet[227], (uint32_t)rules[4 + offset].settings.event.local);
  TF_copy_u8(&packet[231], (uint8_t)(((uint8_t)rules[4 + offset].settings.event.err_level << 5 & 0xe0) | ((uint8_t)rules[4 + offset].settings.should_match_err_level << 4 & 0x10) | ((uint8_t)rules[4 + offset].settings.is_active << 3 & 0x8) | ((uint8_t)rules[4 + offset].settings.condition.type << 0 & 0x7)));
  TF_copy_u8(&packet[232], (uint8_t)rules[5 + offset].settings.event.group);
  TF_copy_u32(&packet[233], (uint32_t)rules[5 + offset].settings.event.local);
  TF_copy_u8(&packet[237], (uint8_t)(((uint8_t)rules[5 + offset].settings.event.err_level << 5 & 0xe0) | ((uint8_t)rules[5 + offset].settings.should_match_err_level << 4 & 0x10) | ((uint8_t)rules[5 + offset].settings.is_active << 3 & 0x8) | ((uint8_t)rules[5 + offset].settings.condition.type << 0 & 0x7)));
  TF_copy_u8(&packet[242], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->group);
  TF_copy_u32(&packet[243], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->local);
  TF_copy_u32(&packet[247], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->time.total_cycle);
  TF_copy_u8(&packet[251], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->time.step);
  TF_copy_u32(&packet[252], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 0)->note);
  TF_copy_u8(&packet[256], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->group);
  TF_copy_u32(&packet[257], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->local);
  TF_copy_u32(&packet[261], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->time.total_cycle);
  TF_copy_u8(&packet[265], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->time.step);
  TF_copy_u32(&packet[266], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 1)->note);
  TF_copy_u8(&packet[270], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->group);
  TF_copy_u32(&packet[271], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->local);
  TF_copy_u32(&packet[275], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->time.total_cycle);
  TF_copy_u8(&packet[279], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->time.step);
  TF_copy_u32(&packet[280], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 2)->note);
  TF_copy_u8(&packet[284], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->group);
  TF_copy_u32(&packet[285], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->local);
  TF_copy_u32(&packet[289], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->time.total_cycle);
  TF_copy_u8(&packet[293], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->time.step);
  TF_copy_u32(&packet[294], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_HIGH, 3)->note);
  TF_copy_u8(&packet[298], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->group);
  TF_copy_u32(&packet[299], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->local);
  TF_copy_u32(&packet[303], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->time.total_cycle);
  TF_copy_u8(&packet[307], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->time.step);
  TF_copy_u32(&packet[308], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 0)->note);
  TF_copy_u8(&packet[312], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->group);
  TF_copy_u32(&packet[313], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->local);
  TF_copy_u32(&packet[317], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->time.total_cycle);
  TF_copy_u8(&packet[321], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->time.step);
  TF_copy_u32(&packet[322], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 1)->note);
  TF_copy_u8(&packet[326], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->group);
  TF_copy_u32(&packet[327], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->local);
  TF_copy_u32(&packet[331], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->time.total_cycle);
  TF_copy_u8(&packet[335], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->time.step);
  TF_copy_u32(&packet[336], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 2)->note);
  TF_copy_u8(&packet[340], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->group);
  TF_copy_u32(&packet[341], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->local);
  TF_copy_u32(&packet[345], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->time.total_cycle);
  TF_copy_u8(&packet[349], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->time.step);
  TF_copy_u32(&packet[350], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_MIDDLE, 3)->note);
  TF_copy_u8(&packet[354], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->group);
  TF_copy_u32(&packet[355], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->local);
  TF_copy_u32(&packet[359], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->time.total_cycle);
  TF_copy_u8(&packet[363], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->time.step);
  TF_copy_u32(&packet[364], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 0)->note);
  TF_copy_u8(&packet[368], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->group);
  TF_copy_u32(&packet[369], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->local);
  TF_copy_u32(&packet[373], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->time.total_cycle);
  TF_copy_u8(&packet[377], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->time.step);
  TF_copy_u32(&packet[378], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 1)->note);
  TF_copy_u8(&packet[382], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->group);
  TF_copy_u32(&packet[383], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->local);
  TF_copy_u32(&packet[387], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->time.total_cycle);
  TF_copy_u8(&packet[391], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->time.step);
  TF_copy_u32(&packet[392], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 2)->note);
  TF_copy_u8(&packet[396], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->group);
  TF_copy_u32(&packet[397], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->local);
  TF_copy_u32(&packet[401], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->time.total_cycle);
  TF_copy_u8(&packet[405], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->time.step);
  TF_copy_u32(&packet[406], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 3)->note);
  TF_copy_u8(&packet[410], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->group);
  TF_copy_u32(&packet[411], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->local);
  TF_copy_u32(&packet[415], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->time.total_cycle);
  TF_copy_u8(&packet[419], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->time.step);
  TF_copy_u32(&packet[420], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 4)->note);
  TF_copy_u8(&packet[424], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->group);
  TF_copy_u32(&packet[425], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->local);
  TF_copy_u32(&packet[429], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->time.total_cycle);
  TF_copy_u8(&packet[433], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->time.step);
  TF_copy_u32(&packet[434], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_LOW, 5)->note);
  TF_copy_u8(&packet[438], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->group);
  TF_copy_u32(&packet[439], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->local);
  TF_copy_u32(&packet[443], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->time.total_cycle);
  TF_copy_u8(&packet[447], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->time.step);
  TF_copy_u32(&packet[448], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 0)->note);
  TF_copy_u8(&packet[452], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->group);
  TF_copy_u32(&packet[453], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->local);
  TF_copy_u32(&packet[457], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->time.total_cycle);
  TF_copy_u8(&packet[461], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->time.step);
  TF_copy_u32(&packet[462], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 1)->note);
  TF_copy_u8(&packet[466], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->group);
  TF_copy_u32(&packet[467], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->local);
  TF_copy_u32(&packet[471], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->time.total_cycle);
  TF_copy_u8(&packet[475], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->time.step);
  TF_copy_u32(&packet[476], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 2)->note);
  TF_copy_u8(&packet[480], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->group);
  TF_copy_u32(&packet[481], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->local);
  TF_copy_u32(&packet[485], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->time.total_cycle);
  TF_copy_u8(&packet[489], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->time.step);
  TF_copy_u32(&packet[490], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EL, 3)->note);
  TF_copy_u8(&packet[494], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->group);
  TF_copy_u32(&packet[495], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->local);
  TF_copy_u32(&packet[499], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->time.total_cycle);
  TF_copy_u8(&packet[503], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->time.step);
  TF_copy_u32(&packet[504], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 0)->note);
  TF_copy_u8(&packet[508], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->group);
  TF_copy_u32(&packet[509], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->local);
  TF_copy_u32(&packet[513], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->time.total_cycle);
  TF_copy_u8(&packet[517], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->time.step);
  TF_copy_u32(&packet[518], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 1)->note);
  TF_copy_u8(&packet[522], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->group);
  TF_copy_u32(&packet[523], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->local);
  TF_copy_u32(&packet[527], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->time.total_cycle);
  TF_copy_u8(&packet[531], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->time.step);
  TF_copy_u32(&packet[532], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 2)->note);
  TF_copy_u8(&packet[536], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->group);
  TF_copy_u32(&packet[537], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->local);
  TF_copy_u32(&packet[541], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->time.total_cycle);
  TF_copy_u8(&packet[545], (uint8_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->time.step);
  TF_copy_u32(&packet[546], (uint32_t)EL_get_the_nth_tlog_from_the_latest(EL_ERROR_LEVEL_EH, 3)->note);
# endif

  *len = 550;
  return TF_TLM_FUNC_ACK_SUCCESS;
}

static TF_TLM_FUNC_ACK Tlm_AOBC_AOBC_(uint8_t* packet, uint16_t* len, uint16_t max_len)
{
  return AOBC_pick_up_tlm_buffer(aobc_driver, AOBC_Tlm_CODE_AOBC_AOBC, packet, len, max_len);
}

static TF_TLM_FUNC_ACK Tlm_AOBC_HK_(uint8_t* packet, uint16_t* len, uint16_t max_len)
{
  return AOBC_pick_up_tlm_buffer(aobc_driver, AOBC_Tlm_CODE_AOBC_HK, packet, len, max_len);
}

# pragma section
