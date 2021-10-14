

[TOC]

# 模型定义



## 用户信息定义

### 用户信息表

#### 表名

user_tab

#### 定义

| 名称       | 描述     | 类型    | 长度 | 值域                                    | 备注 |
| ---------- | -------- | ------- | ---- | --------------------------------------- | ---- |
| id         | 用户id   | integer |      |                                         | pk   |
| username   | 用户名   | string  | 32   |                                         | uk   |
| password   | 密码     | string  | 128  |                                         |      |
| createdate | 创建时间 | integer |      |                                         |      |
| gender     | 性别     | integer |      | 0: others <br />1: female <br />2: male |      |
| birthday   | 生日     | integer |      |                                         |      |
| email      | 邮箱     | string  | 128  |                                         |      |
| mobile     | 手机号   | string  | 11   |                                         |      |



### 家庭信息表

#### 表名

family_tab

#### 定义

| 名称        | 描述     | 类型    | 长度 | 值域 | 备注 |
| ----------- | -------- | ------- | ---- | ---- | ---- |
| id          | 家庭id   | integer |      |      | pk   |
| description | 家庭描述 | string  | 32   |      |      |
| address     | 家庭地址 | string  | 128  |      |      |



### 用户家庭映射表

#### 表名

user_family_tab

#### 定义

| 名称      | 描述   | 类型    | 长度 | 值域          | 备注  |
| --------- | ------ | ------- | ---- | ------------- | ----- |
| user_id   | 用户id | integer |      | user_tab.id   | pk,fk |
| family_id | 家庭id | integer |      | family_tab.id | pk,fk |



## 账本信息定义

### 用户钱包表

#### 表名

user_wallet_tab

#### 定义

| 名称   | 描述   | 类型    | 长度 | 值域        | 备注  |
| ------ | ------ | ------- | ---- | ----------- | ----- |
| id     | 钱包id | integer |      | user_tab.id | pk,fk |
| debt   | 负债   | double  |      |             |       |
| asset  | 总资产 | double  |      |             |       |
| lend   | 借出   | double  |      |             |       |
| borrow | 借入   | double  |      |             |       |



### 用户账户表

#### 表名

account_tab

#### 定义

| 名称        | 描述     | 类型    | 长度 | 值域                     | 备注 |
| ----------- | -------- | ------- | ---- | ------------------------ | ---- |
| id          | 账户id   | integer |      |                          | pk   |
| user_id     | 钱包id   | integer |      | user_tab.id              | fk   |
| description | 描述     | string  | 128  |                          |      |
| type        | 类型     | integer |      | 0: 信用卡<br />1: 储蓄卡 |      |
| bank        | 银行编号 | string  | 10   |                          |      |
| card        | 卡号     | string  | 20   |                          |      |
| asset       | 资产     | double  |      |                          |      |



### 账本表

#### 表名

account_book_tab

#### 定义

| 名称        | 描述                   | 类型    | 长度 | 值域          | 备注 |
| ----------- | ---------------------- | ------- | ---- | ------------- | ---- |
| id          | 账户id                 | integer |      | family_tab.id | pk   |
| description | 描述                   | string  | 32   |               |      |
| category    | 账单记录分类json字符串 | string  | 1024 |               |      |



### 账单表

#### 表名

bill_tab

#### 定义

| 名称       | 描述                                 | 类型    | 长度 | 值域                                                         | 备注 |
| ---------- | ------------------------------------ | ------- | ---- | ------------------------------------------------------------ | ---- |
| id         | 账单id                               | string  | 10   |                                                              | pk   |
| user_id    | 所属钱包id                           | integer |      | user_tab.id                                                  | fk   |
| account_id | 所属账户                             | integer |      | account_tab.id                                               | fk   |
| book_id    | 所属账本                             | integer |      | account_book_tab.id                                          | fk   |
| time       | 时间                                 | integer |      |                                                              |      |
| type       | 账单类型                             | integer |      | 0: 收入<br />1: 支出<br />2: 借入<br />3: 借出<br />4: 转入<br />5: 转出<br />6: 自转 |      |
| category   | 分类                                 | string  | 10   |                                                              |      |
| remark     | 类型                                 | string  | 20   | 数组，逗号分开                                               |      |
| amount     | 金额                                 | double  |      |                                                              |      |
| comment    | 备注信息                             | string  | 128  |                                                              |      |
| confirm    | 确认标记，转帐、借出、借入完成后确认 | boolean |      |                                                              |      |
| user1_id   | 对方用户，转帐时使用                 | integer |      | user_tab.id                                                  | fk   |
| user2_id   | 其他用户                             | integer |      | user_tab.id                                                  | fk   |
| asset1     | 其他金额，收款金额                   | double  |      |                                                              |      |
| asset2     | 其他金额                             | double  |      |                                                              |      |













