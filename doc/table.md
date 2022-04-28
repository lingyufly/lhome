

[TOC]

# 模型定义



## 用户信息定义

### 用户信息表

#### 表名

user_tab

#### 定义

| 名称        | 描述       | 类型    | 长度 | 值域                            | 备注 |
| ----------- | ---------- | ------- | ---- | ------------------------------- | ---- |
| id          | 用户id     | integer |      |                                 | pk   |
| name        | 用户名     | string  | 32   |                                 | uk   |
| password    | 密码       | string  | 128  |                                 |      |
| photo       | 头像文件名 | string  | 128  |                                 |      |
| create_time | 创建时间   | integer |      |                                 |      |
| gender      | 性别       | integer |      | 0: 未知 <br />1: 男 <br />2: 女 |      |
| birthday    | 生日       | Date    |      |                                 |      |
| email       | 邮箱       | string  | 128  |                                 |      |
| mobile      | 手机号     | string  | 11   |                                 |      |



### 组信息表

#### 表名

group_tab

#### 定义

| 名称        | 描述       | 类型    | 长度 | 值域 | 备注 |
| ----------- | ---------- | ------- | ---- | ---- | ---- |
| id          | 组id       | integer |      |      | pk   |
| name        | 组名称     | string  | 32   |      | uk   |
| create_time | 创建日期   | integer |      |      |      |
| photo       | 头像文件名 | string  | 128  |      |      |



### 用户组映射表

#### 表名

user_group_tab

#### 定义

| 名称     | 描述   | 类型    | 长度 | 值域         | 备注  |
| -------- | ------ | ------- | ---- | ------------ | ----- |
| user_id  | 用户id | integer |      | user_tab.id  | pk,fk |
| group_id | 组id   | integer |      | group_tab.id | pk,fk |



## 账本信息定义

### 用户钱包表

#### 表名

wallet_tab

#### 定义

| 名称   | 描述   | 类型    | 长度 | 值域        | 备注  |
| ------ | ------ | ------- | ---- | ----------- | ----- |
| id     | 钱包id | integer |      | user_tab.id | pk,fk |
| asset  | 总资产 | double  |      |             |       |
| debt   | 负债   | double  |      |             |       |
| lend   | 借出   | double  |      |             |       |
| borrow | 借入   | double  |      |             |       |



### 用户账户表

#### 表名

account_tab

#### 定义

| 名称        | 描述     | 类型    | 长度 | 值域        | 备注 |
| ----------- | -------- | ------- | ---- | ----------- | ---- |
| id          | 账户id   | integer |      |             | pk   |
| user_id     | 钱包id   | integer |      | user_tab.id | fk   |
| name        | 描述     | string  | 32   |             |      |
| photo       | 照片     | string  | 128  |             |      |
| asset       | 资产     | double  |      |             |      |
| create_time | 创建日期 | integer |      |             |      |



### 账本表

#### 表名

account_book_tab

#### 定义

| 名称     | 描述                   | 类型    | 长度 | 值域         | 备注  |
| -------- | ---------------------- | ------- | ---- | ------------ | ----- |
| id       | 账本id                 | integer |      | group_tab.id | pk,fk |
| category | 账单记录分类json字符串 | string  | 1024 |              |       |



### 账单表

#### 表名

bill_tab

#### 定义

| 名称        | 描述                                 | 类型    | 长度 | 值域                                                         | 备注 |
| ----------- | ------------------------------------ | ------- | ---- | ------------------------------------------------------------ | ---- |
| id          | 账单id                               | integer |      |                                                              | pk   |
| user_id     | 所属钱包id                           | integer |      | user_tab.id                                                  | fk   |
| account_id  | 所属账户                             | integer |      | account_tab.id                                               | fk   |
| book_id     | 所属账本                             | integer |      | account_book_tab.id                                          | fk   |
| create_time | 时间                                 | integer |      |                                                              |      |
| bill_type   | 账单类型                             | integer |      | 0: 收入<br />1: 支出<br />2: 借入<br />3: 借出<br />4: 转入<br />5: 转出<br />6: 自转 |      |
| category    | 分类                                 | string  | 32   |                                                              |      |
| tag         | 类型                                 | string  | 32   |                                                              |      |
| amount      | 金额                                 | double  |      |                                                              |      |
| comment     | 备注信息                             | string  | 128  |                                                              |      |
| confirm     | 确认标记，转帐、借出、借入完成后确认 | bool    |      |                                                              |      |
| r_user_id   | 对方用户，转帐时使用                 | integer |      | user_tab.id                                                  | fk   |
| r_bill_id   | 对方记录                             | integer |      | bill_tab.id                                                  | fk   |













