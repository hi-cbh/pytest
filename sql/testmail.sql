/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : localhost
 Source Database       : testmail

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : utf-8

 Date: 11/16/2017 11:44:45 AM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `tb_app_cpu_mem`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_cpu_mem`;
CREATE TABLE `tb_app_cpu_mem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL,
  `versionID` int(11) NOT NULL,
  `networkType` varchar(20) NOT NULL,
  `nowTime` timestamp NOT NULL DEFAULT '2016-09-12 14:38:32',
  `avgcpu` decimal(9,4) NOT NULL COMMENT 'cpu峰值',
  `maxcpu` decimal(9,4) NOT NULL COMMENT '平均cpu值',
  `avgmem` decimal(9,2) NOT NULL COMMENT '内存峰值',
  `maxmem` decimal(9,2) NOT NULL COMMENT '平均内存',
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8 COMMENT='资源消耗流量';

-- ----------------------------
--  Table structure for `tb_app_data_timedelay`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_data_timedelay`;
CREATE TABLE `tb_app_data_timedelay` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL COMMENT '产品名称',
  `versionID` int(11) NOT NULL COMMENT '版本ID',
  `networkType` varchar(20) NOT NULL COMMENT '网络类型',
  `nowTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '运行时间',
  `logintime` decimal(9,2) NOT NULL COMMENT '登陆时延',
  `receivetime` decimal(9,2) NOT NULL COMMENT '接收时延',
  `readtime` decimal(9,2) NOT NULL COMMENT '打开未读时延',
  `downtime` decimal(9,2) NOT NULL COMMENT '发送时延',
  `sendtime` decimal(9,2) NOT NULL COMMENT '下载时延',
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=578 DEFAULT CHARSET=utf8 COMMENT='时延原始数据';

-- ----------------------------
--  Table structure for `tb_app_flow_brush`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_flow_brush`;
CREATE TABLE `tb_app_flow_brush` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL,
  `versionID` int(11) NOT NULL,
  `networkType` varchar(20) NOT NULL,
  `nowTime` timestamp NOT NULL DEFAULT '2016-09-12 14:38:32',
  `upflow` decimal(9,2) NOT NULL COMMENT '上传流量',
  `downflow` decimal(9,2) NOT NULL COMMENT '下载流量',
  `allflow` decimal(9,2) NOT NULL COMMENT '总流量',
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8 COMMENT='资源消耗流量';

-- ----------------------------
--  Table structure for `tb_app_flow_login`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_flow_login`;
CREATE TABLE `tb_app_flow_login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL,
  `versionID` int(11) NOT NULL,
  `networkType` varchar(20) NOT NULL,
  `nowTime` timestamp NOT NULL DEFAULT '2016-09-12 14:38:32',
  `upflow` decimal(9,2) NOT NULL COMMENT '总流量',
  `downflow` decimal(9,2) NOT NULL COMMENT '上传流量',
  `allflow` decimal(9,2) NOT NULL COMMENT '下载流量',
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=168 DEFAULT CHARSET=utf8 COMMENT='资源消耗流量';

-- ----------------------------
--  Table structure for `tb_app_prot`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_prot`;
CREATE TABLE `tb_app_prot` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL COMMENT '产品名',
  `versionID` int(11) NOT NULL COMMENT '版本ID',
  `versionName` varchar(255) NOT NULL COMMENT '版本名',
  `tdesc` varchar(255) DEFAULT NULL COMMENT '描述',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_app_standy_email`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_standy_email`;
CREATE TABLE `tb_app_standy_email` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL,
  `versionID` int(11) NOT NULL,
  `networkType` varchar(20) NOT NULL,
  `nowTime` timestamp NOT NULL DEFAULT '2016-09-12 14:38:32',
  `electric` decimal(9,3) NOT NULL COMMENT '电量',
  `upflow` decimal(9,3) NOT NULL COMMENT '上传下载流量',
  `downflow` decimal(9,3) NOT NULL COMMENT '上传流量',
  `allflow` decimal(9,3) NOT NULL COMMENT '下载流量',
  `emailcount` int(9) NOT NULL COMMENT '接收的邮件数量',
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8 COMMENT='待机资源消耗';

-- ----------------------------
--  Table structure for `tb_app_standy_no`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_standy_no`;
CREATE TABLE `tb_app_standy_no` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL,
  `versionID` int(11) NOT NULL,
  `networkType` varchar(20) NOT NULL,
  `nowTime` timestamp NOT NULL DEFAULT '2016-09-12 14:38:32',
  `electric` decimal(9,3) NOT NULL COMMENT '电量',
  `upflow` decimal(9,3) NOT NULL COMMENT '上传下载流量',
  `downflow` decimal(9,3) NOT NULL COMMENT '上传流量',
  `allflow` decimal(9,3) NOT NULL COMMENT '下载流量',
  `avgmem` decimal(9,3) NOT NULL COMMENT '待机内存',
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8 COMMENT='待机资源消耗';

-- ----------------------------
--  Table structure for `tb_app_start_time`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_start_time`;
CREATE TABLE `tb_app_start_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(20) NOT NULL,
  `versionID` int(11) NOT NULL,
  `networkType` varchar(20) NOT NULL,
  `nowTime` timestamp NOT NULL DEFAULT '2016-09-12 14:38:32',
  `time0` decimal(9,3) NOT NULL,
  `time1` decimal(9,3) NOT NULL COMMENT '杀进程启动时间',
  `time2` decimal(9,3) NOT NULL,
  `time3` decimal(9,3) NOT NULL,
  `time4` decimal(9,3) NOT NULL,
  `time5` decimal(9,3) NOT NULL,
  `time6` decimal(9,3) NOT NULL,
  `time7` decimal(9,3) NOT NULL,
  `time8` decimal(9,3) NOT NULL,
  `time9` decimal(9,3) NOT NULL,
  `groupId` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf8 COMMENT='资源消耗流量';

-- ----------------------------
--  Table structure for `tb_app_value`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_value`;
CREATE TABLE `tb_app_value` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `productName` varchar(255) DEFAULT NULL COMMENT '产品名',
  `versionID` int(12) DEFAULT NULL COMMENT '版本ID',
  `networkType` varchar(255) DEFAULT NULL COMMENT '网络状态',
  `logintime` decimal(9,2) DEFAULT NULL COMMENT '登录时延',
  `receivetime` decimal(9,2) DEFAULT NULL COMMENT '接收本域邮件时延',
  `readtime` decimal(9,2) DEFAULT NULL COMMENT '打开未读邮件时延',
  `sendtime` decimal(9,2) DEFAULT NULL COMMENT '发送邮件时延',
  `downtime` decimal(9,2) DEFAULT NULL COMMENT '下载附件时延',
  `loginflow` decimal(9,2) DEFAULT NULL COMMENT '首次登录流量',
  `brushflow` decimal(9,2) DEFAULT NULL COMMENT '空刷流量',
  `standynoelectric` decimal(9,2) DEFAULT NULL COMMENT '待机无邮件电量',
  `standynoflow` decimal(9,2) DEFAULT NULL COMMENT '待机无邮件流量',
  `standyelectric` decimal(9,2) DEFAULT NULL COMMENT '待机有邮件电量',
  `standyflow` decimal(9,2) DEFAULT NULL COMMENT '待机有邮件流量',
  `maxmem` decimal(9,2) DEFAULT NULL COMMENT '业务运行内存峰值',
  `maxcpu` decimal(9,2) DEFAULT NULL COMMENT 'CPU峰值',
  `avgmem` decimal(9,2) DEFAULT NULL COMMENT '待机平均内存',
  `avgtime` decimal(9,2) DEFAULT NULL COMMENT '杀进程启动时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `tb_app_value_all`
-- ----------------------------
DROP TABLE IF EXISTS `tb_app_value_all`;
CREATE TABLE `tb_app_value_all` (
  `id` int(8) NOT NULL AUTO_INCREMENT,
  `productName` varchar(255) DEFAULT NULL COMMENT '产品名',
  `versionID` int(12) DEFAULT NULL COMMENT '版本ID',
  `networkType` varchar(255) DEFAULT NULL COMMENT '网络状态',
  `logintime` decimal(9,2) DEFAULT NULL COMMENT '登录时延',
  `receivetime` decimal(9,2) DEFAULT NULL COMMENT '接收本域邮件时延',
  `readtime` decimal(9,2) DEFAULT NULL COMMENT '打开未读邮件时延',
  `downtime` decimal(9,2) DEFAULT NULL COMMENT '下载附件时延',
  `sendtime` decimal(9,2) DEFAULT NULL COMMENT '发送邮件时延',
  `loginflow` decimal(9,2) DEFAULT NULL COMMENT '首次登录流量',
  `brushflow` decimal(9,2) DEFAULT NULL COMMENT '空刷流量',
  `standynoelectric` decimal(9,2) DEFAULT NULL COMMENT '待机无邮件电量',
  `standynoflow` decimal(9,2) DEFAULT NULL COMMENT '待机无邮件流量',
  `standyelectric` decimal(9,2) DEFAULT NULL COMMENT '待机有邮件电量',
  `standyflow` decimal(9,2) DEFAULT NULL COMMENT '待机有邮件流量',
  `maxmem` decimal(9,2) DEFAULT NULL COMMENT '业务运行内存峰值',
  `maxcpu` decimal(9,2) DEFAULT NULL COMMENT 'CPU峰值',
  `avgmem` decimal(9,2) DEFAULT NULL COMMENT '待机平均内存',
  `avgtime` decimal(9,2) DEFAULT NULL COMMENT '杀进程启动时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
