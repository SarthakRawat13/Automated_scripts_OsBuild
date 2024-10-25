/* TOPAZ_CONFIGURATION for IIC3, IIC4, SPI, BOARD REVISION:NULL
 */

#include <common.h>
#include <i2c.h>
#include <fdt_support.h>
#include <init.h>
#include <asm/global_data.h>
#include <asm/io.h>
#include <asm/arch/clock.h>
#include <asm/arch/fsl_serdes.h>
#include <asm/arch/soc.h>
#include <asm/arch-fsl-layerscape/fsl_icid.h>
#include <hwconfig.h>
#include <ahci.h>
#include <mmc.h>
#include <scsi.h>
#include <fm_eth.h>
#include <fsl_csu.h>
#include <fsl_esdhc.h>
#include <fsl_dspi.h>
#include <asm-generic/gpio.h>
#include <asm/arch/gpio.h>

#define LS1046A_PORSR1_REG 0x1EE0000
#define BOOT_SRC_SD        0x20000000
#define BOOT_SRC_MASK	   0xFF800000

#define BYTE_SWAP_32(word)  ((((word) & 0xff000000) >> 24) |  \
(((word) & 0x00ff0000) >>  8) | \
(((word) & 0x0000ff00) <<  8) | \
(((word) & 0x000000ff) << 24))
#define SPI_MCR_REG	0x2100000

/*TOPAZ GPIO configuration
*/
#define GPIO_M2_RST_EN 19
#define GPIO_ETH_RST 20
// #define GPIO_eMMC_SEL 21
#define GPIO_ZES_EBIT 22
#define GPIO_M2_RST_1 35
#define GPIO_M2_RST_2 34
// #define GPIO_M2_RST_3 33

DECLARE_GLOBAL_DATA_PTR;




static inline void set_spi_cs_signal_inactive(void)
{
	/* default: all CS signals inactive state is high */
	uint mcr_val;
	uint mcr_cfg_val = DSPI_MCR_MSTR | DSPI_MCR_PCSIS_MASK |
				DSPI_MCR_CRXF | DSPI_MCR_CTXF;

	mcr_val = in_be32(SPI_MCR_REG);
	mcr_val |= DSPI_MCR_HALT;
	out_be32(SPI_MCR_REG, mcr_val);
	out_be32(SPI_MCR_REG, mcr_cfg_val);
	mcr_val = in_be32(SPI_MCR_REG);
	mcr_val &= ~DSPI_MCR_HALT;
	out_be32(SPI_MCR_REG, mcr_val);
}

int board_early_init_f(void)
{
	fsl_lsch2_early_init_f();

	return 0;
}


int checkboard(void)
{
	static const char *freq[2] = {"100.00MHZ", "100.00MHZ"};
	u32 boot_src;

	boot_src = BYTE_SWAP_32(readl(LS1046A_PORSR1_REG));

	if ((boot_src & BOOT_SRC_MASK) == BOOT_SRC_SD)
		puts("SD\n");
	else
		puts("QSPI\n");
	printf("SD1_CLK1 = %s, SD1_CLK2 = %s\n", freq[0], freq[1]);

	return 0;
}

int board_init(void)
{

int zese, eth, m2rst, asic1, asic2;

    // Request control of the GPIO
    zese = gpio_request(GPIO_ZES_EBIT, "zese_gpio");
    if (zese) {
        printf("Failed to request GPIO %d\n", GPIO_ZES_EBIT);
        return zese;
    }

    // Set the GPIO direction to output
    zese = gpio_direction_input(GPIO_ZES_EBIT);
    if (zese) {
        printf("Failed to set GPIO direction for GPIO %d\n", GPIO_ZES_EBIT);
        gpio_free(GPIO_ZES_EBIT);
        return zese;
    }


    // Request control of the GPIO
    eth = gpio_request(GPIO_ETH_RST, "gpio_output");
    if (eth) {
        printf("Failed to request GPIO %d\n", GPIO_ETH_RST);
        return eth;
    }

    // Set the GPIO direction to output
    eth = gpio_direction_output(GPIO_ETH_RST, 0);
    if (eth) {
        printf("Failed to set GPIO direction for GPIO %d\n", GPIO_ETH_RST);
        gpio_free(GPIO_ETH_RST);
        return eth;
    }

    // Set the GPIO value to high (1)
    gpio_set_value(GPIO_ETH_RST, 1); // Setting it high
    printf("GPIO %d initialized to high\n", GPIO_ETH_RST);
    
    // Request control of the GPIO
    m2rst = gpio_request(GPIO_M2_RST_EN, "gpio_output");
    if (m2rst) {
        printf("Failed to request GPIO %d\n", GPIO_M2_RST_EN);
        return m2rst;
    }

    // Set the GPIO direction to output
    m2rst = gpio_direction_output(GPIO_M2_RST_EN, 0);
    if (m2rst) {
        printf("Failed to set GPIO direction for GPIO %d\n", GPIO_M2_RST_EN);
        gpio_free(GPIO_M2_RST_EN);
        return m2rst;
    }

    // Set the GPIO value to high (1)
    gpio_set_value(GPIO_M2_RST_EN, 1); // Setting it high
    printf("GPIO %d initialized to high\n", GPIO_M2_RST_EN);
    
    
    
    
    // Request control of the GPIO
    asic1 = gpio_request(GPIO_M2_RST_1, "gpio_output");
    if (asic1) {
        printf("Failed to request GPIO %d\n", GPIO_M2_RST_1);
        return asic1;
    }

    // Set the GPIO direction to output
    asic1 = gpio_direction_output(GPIO_M2_RST_1, 0);
    if (asic1) {
        printf("Failed to set GPIO direction for GPIO %d\n", GPIO_M2_RST_1);
        gpio_free(GPIO_M2_RST_1);
        return asic1;
    }

    // Set the GPIO value to high (1)
    gpio_set_value(GPIO_M2_RST_1, 1); // Setting it high
    printf("GPIO %d initialized to high\n", GPIO_M2_RST_1);
    
    
    
    
     // Request control of the GPIO
    asic2 = gpio_request(GPIO_M2_RST_2, "gpio_output");
    if (asic2) {
        printf("Failed to request GPIO %d\n", GPIO_M2_RST_2);
        return asic2;
    }

    // Set the GPIO direction to output
    asic2 = gpio_direction_output(GPIO_M2_RST_2, 0);
    if (asic2) {
        printf("Failed to set GPIO direction for GPIO %d\n", GPIO_M2_RST_2);
        gpio_free(GPIO_M2_RST_2);
        return asic2;
    }

    // Set the GPIO value to high (1)
    gpio_set_value(GPIO_M2_RST_2, 1); // Setting it high
    printf("GPIO %d initialized to high\n", GPIO_M2_RST_2);
    
    
    
    
    
     // Request control of the GPIO
//    asic3 = gpio_request(GPIO_M2_RST_3, "gpio_output");
//    if (asic3) {
//        printf("Failed to request GPIO %d\n", GPIO_M2_RST_3);
//        return asic3;
//    }

    // Set the GPIO direction to output
//    asic3 = gpio_direction_output(GPIO_M2_RST_3, 0);
//    if (asic3) {
//        printf("Failed to set GPIO direction for GPIO %d\n", GPIO_M2_RST_3);
//        gpio_free(GPIO_M2_RST_3);
//        return asic3;
//    }

    // Set the GPIO value to high (1)
//    gpio_set_value(GPIO_M2_RST_3, 1); // Setting it high
//    printf("GPIO %d initialized to high\n", GPIO_M2_RST_3);
      
    return 0;

}

int board_setup_core_volt(u32 vdd)
{
	return 0;
}

void config_board_mux(void)
{
#ifdef CONFIG_HAS_FSL_XHCI_USB
	struct ccsr_scfg *scfg = (struct ccsr_scfg *)CONFIG_SYS_FSL_SCFG_ADDR;
	u32 usb_pwrfault;
	/*
	 * USB3 is not used, configure mux to IIC4_SCL/IIC4_SDA
	 */

	/* IIC3 is used, configure mux to use IIC3_SCL/IIC3/SDA */
	out_be32(&scfg->rcwpmuxcr0, 0x0000);
	
	out_be32(&scfg->usbdrvvbus_selcr, SCFG_USBDRVVBUS_SELCR_USB1);
	usb_pwrfault = (SCFG_USBPWRFAULT_SHARED <<
			SCFG_USBPWRFAULT_USB1_SHIFT);
	out_be32(&scfg->usbpwrfault_selcr, usb_pwrfault);

#endif
	set_spi_cs_signal_inactive();
}

#ifdef CONFIG_MISC_INIT_R
int misc_init_r(void)
{
	config_board_mux();
	return 0;
}
#endif

int ft_board_setup(void *blob, struct bd_info *bd)
{
	u64 base[CONFIG_NR_DRAM_BANKS];
	u64 size[CONFIG_NR_DRAM_BANKS];

	/* fixup DT for the two DDR banks */
	base[0] = gd->bd->bi_dram[0].start;
	size[0] = gd->bd->bi_dram[0].size;
	base[1] = gd->bd->bi_dram[1].start;
	size[1] = gd->bd->bi_dram[1].size;

	fdt_fixup_memory_banks(blob, base, size, 2);
	ft_cpu_setup(blob, bd);

#ifdef CONFIG_SYS_DPAA_FMAN
#ifndef CONFIG_DM_ETH
	fdt_fixup_fman_ethernet(blob);
#endif
#endif

	fdt_fixup_icid(blob);

	return 0;
}
