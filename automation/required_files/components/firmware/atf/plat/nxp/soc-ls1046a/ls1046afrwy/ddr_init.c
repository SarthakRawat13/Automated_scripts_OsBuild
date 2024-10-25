/*
 * Topaz_DDR_INIT_2100
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

#include <assert.h>
#include <errno.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <common/debug.h>
#include <ddr.h>
#include <errata.h>
#include <lib/utils.h>

#include "plat_common.h"
#include <platform_def.h>

#ifdef CONFIG_STATIC_DDR
const struct ddr_cfg_regs static_2100 = {
	.cs[0].config = 0x80010512,
	.cs[0].bnds = 0xFF,
	.sdram_cfg[0] = 0x452C0000,
	.sdram_cfg[1] = 0x00401030,
	.sdram_cfg[2] = 0x2000,
	.timing_cfg[0] = 0x80770010,
	.timing_cfg[1] = 0x28221063,
	.timing_cfg[2] = 0x005911A5,
	.timing_cfg[3] = 0x125D2100,
	.timing_cfg[4] = 0x02,
	.timing_cfg[5] = 0x09401400,
	.timing_cfg[6] = 0x0,
	.timing_cfg[7] = 0x25540000,
	.timing_cfg[8] = 0x08227800,
	.timing_cfg[9] = 0x0,
	.dq_map[0] = 0x0,
	.dq_map[1] = 0x0,
	.dq_map[2] = 0x0,
	.dq_map[3] = 0x0,
	.sdram_mode[0] = 0x01010640,
	.sdram_mode[1] = 0x00100000,
	.sdram_mode[8] = 0x0B01,
	.sdram_mode[9] = 0x08800000,
	.interval = 0x1FFE07FF,
	.zq_cntl = 0x8A090705,
	.ddr_sr_cntr = 0x0,
	.clk_cntl = 0x02400000,
	.cdr[0] = 0x80080000,
	.cdr[1] = 0x80,
	.wrlvl_cntl[0] = 0x86750604,
	.wrlvl_cntl[1] = 0x05050604,
	.wrlvl_cntl[2] = 0x04040404,
};

long long board_static_ddr(struct ddr_info *priv)
{
	printf("++TOPAZ_240620_eth_in_dts_++++++++++++++++\n");
	printf("board_static_ddr\n");
	memcpy(&priv->ddr_reg, &static_2100, sizeof(static_2100));

	return 0x100000000ULL;
}

#endif

long long init_ddr(void)
{
	int spd_addr[] = { 0x51, 0x52, 0x53, 0x54 };
	struct ddr_info info;
	struct sysinfo sys;
	long long dram_size;

	zeromem(&sys, sizeof(sys));
	if (get_clocks(&sys)) {
		ERROR("System clocks are not set\n");
		assert(0);
	}
	debug("platform clock %lu\n", sys.freq_platform);
	debug("DDR PLL1 %lu\n", sys.freq_ddr_pll0);
	debug("DDR PLL2 %lu\n", sys.freq_ddr_pll1);

	zeromem(&info, sizeof(struct ddr_info));
	info.num_ctlrs = 1;
	info.dimm_on_ctlr = 1;
	info.clk = get_ddr_freq(&sys, 0);
	info.spd_addr = spd_addr;
	info.ddr[0] = (void *)NXP_DDR_ADDR;

	dram_size = dram_init(&info);

	if (dram_size < 0)
		ERROR("DDR init failed.\n");

	erratum_a008850_post();

	return dram_size;
}

