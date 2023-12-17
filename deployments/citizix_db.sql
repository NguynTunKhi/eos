/*
 Navicat Premium Data Transfer

 Source Server         : eos-db
 Source Server Type    : MySQL
 Source Server Version : 100708
 Source Host           : 10.0.12.53:3306
 Source Schema         : citizix_db

 Target Server Type    : MySQL
 Target Server Version : 100708
 File Encoding         : 65001

 Date: 04/04/2023 06:05:42
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for scheduler_run
-- ----------------------------
DROP TABLE IF EXISTS `scheduler_run`;
CREATE TABLE `scheduler_run` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` int(11) DEFAULT NULL,
  `status` varchar(512) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  `run_output` longtext DEFAULT NULL,
  `run_result` longtext DEFAULT NULL,
  `traceback` longtext DEFAULT NULL,
  `worker_name` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_id__idx` (`task_id`),
  CONSTRAINT `scheduler_run_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `scheduler_task` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- ----------------------------
-- Records of scheduler_run
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for scheduler_task
-- ----------------------------
DROP TABLE IF EXISTS `scheduler_task`;
CREATE TABLE `scheduler_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `application_name` varchar(512) DEFAULT NULL,
  `task_name` varchar(512) DEFAULT NULL,
  `group_name` varchar(512) DEFAULT NULL,
  `status` varchar(512) DEFAULT NULL,
  `broadcast` char(1) DEFAULT NULL,
  `function_name` varchar(512) DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  `args` longtext DEFAULT NULL,
  `vars` longtext DEFAULT NULL,
  `enabled` char(1) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `next_run_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  `repeats` int(11) DEFAULT NULL,
  `retry_failed` int(11) DEFAULT NULL,
  `period` int(11) DEFAULT NULL,
  `prevent_drift` char(1) DEFAULT NULL,
  `cronline` varchar(512) DEFAULT NULL,
  `timeout` int(11) DEFAULT NULL,
  `sync_output` int(11) DEFAULT NULL,
  `times_run` int(11) DEFAULT NULL,
  `times_failed` int(11) DEFAULT NULL,
  `last_run_time` datetime DEFAULT NULL,
  `assigned_worker_name` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- ----------------------------
-- Records of scheduler_task
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for scheduler_task_deps
-- ----------------------------
DROP TABLE IF EXISTS `scheduler_task_deps`;
CREATE TABLE `scheduler_task_deps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(512) DEFAULT NULL,
  `task_parent` int(11) DEFAULT NULL,
  `task_child` int(11) DEFAULT NULL,
  `can_visit` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_child__idx` (`task_child`),
  CONSTRAINT `scheduler_task_deps_ibfk_1` FOREIGN KEY (`task_child`) REFERENCES `scheduler_task` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- ----------------------------
-- Records of scheduler_task_deps
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for scheduler_worker
-- ----------------------------
DROP TABLE IF EXISTS `scheduler_worker`;
CREATE TABLE `scheduler_worker` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `worker_name` varchar(255) DEFAULT NULL,
  `first_heartbeat` datetime DEFAULT NULL,
  `last_heartbeat` datetime DEFAULT NULL,
  `status` varchar(512) DEFAULT NULL,
  `is_ticker` char(1) DEFAULT NULL,
  `group_names` longtext DEFAULT NULL,
  `worker_stats` longtext DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `worker_name` (`worker_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;

-- ----------------------------
-- Records of scheduler_worker
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
