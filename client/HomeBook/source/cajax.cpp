/*************************************************************************
  > File Name:      cajax.cpp
  > Author:         ly
  > Created Time:   Sat 23 Oct 2021 09:43:53 PM CST
  > Description:    封装的http请求接口
 ************************************************************************/

#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QThread>
#include <QJSEngine>
#include <QJsonObject>
#include <QVariant>
#include <QJsonDocument>
#include <QTimer>
#include <QTextCodec>
#include <QDebug>
#include <QHttpMultiPart>
#include <QFile>
#include <QFileInfo>

#include "cajax.h"

// 全局的请求管理类
QNetworkAccessManager CAjax::s_qNetworkManager;

// 全局的请求根地址
QString CAjax::s_qServerUrl;

// 超时时间 ms
int CAjax::s_iTimeoutMs;

/**
 * @brief QReplyTimeout::QReplyTimeout http请求超时封装类
 * @param parent
 * @param timeout
 * 使用方法 QReplyTimeout * pTimeout = new QReplyTimeout(pReply, 3000);
 */
QReplyTimeout::QReplyTimeout(QNetworkReply *parent,int timeout) : QObject(parent)
{
    if(parent && parent->isRunning())
    {
        mTimeoutTimer = new QTimer(this);
        mTimeoutTimer->setSingleShot(true);
        connect(mTimeoutTimer, &QTimer::timeout, [=](){
            QNetworkReply *reply = parent;

            if(reply->isRunning())
            {
                reply->abort();
            }
        });
        mTimeoutTimer->start(timeout);
    }
}

QReplyTimeout::~QReplyTimeout()
{

}


/**
 * @brief CAjax::CAjax
 * @param parent
 */
CAjax::CAjax(QObject *parent)
    :QObject(parent)
{
}

/**
 * @brief CAjax::~CAjax
 */
CAjax::~CAjax()
{

}

/**
 * @brief CAjax::setServerUrl
 * @param url
 */
void CAjax::setServerUrl(QString url)
{
    s_qServerUrl=url;
}

/**
 * @brief CAjax::setTimeout
 * @param iMs
 */
void CAjax::setTimeout(int iMs)
{
    s_iTimeoutMs=iMs;
}

/**
 * @brief CAjax::get  get请求接口
 * @param url 请求地址
 * @param jsObj 请求数据
 * @param jsCb 请求回调
 */
void CAjax::get(QString url, QJSValue jsObj, QJSValue jsCb)
{
    if (url.startsWith("/"))
    {
        url=s_qServerUrl+url;
    }

    // 遍历请求的参数，组合到url上
    QJsonDocument doc = QJsonDocument::fromVariant(jsObj.toVariant());
    QJsonObject obj=doc.object();
    QStringList qList;
    for (auto it=obj.begin(); it!=obj.end(); it++)
    {
        QString ss=it.key()+"="+it.value().toVariant().toString();
        qList.append(ss);
    }
    QString getUrl=url+"?"+qList.join('&');

    QNetworkRequest request=QNetworkRequest(getUrl);
    QNetworkReply *pReply = s_qNetworkManager.get(request);

    wait(pReply, jsCb);
}

/**
 * @brief CAjax::post  post请求接口
 * @param url 请求地址
 * @param jsObj 请求数据
 * @param jsCb 请求回调
 */
void CAjax::post(QString url, QJSValue jsObj, QJSValue jsCb)
{
    if (url.startsWith("/"))
    {
        url=s_qServerUrl+url;
    }
    QNetworkRequest request=QNetworkRequest(url);
    request.setRawHeader("Content-Type","application/json");

    QJsonDocument doc = QJsonDocument::fromVariant(jsObj.toVariant());
    QNetworkReply *pReply = s_qNetworkManager.post(request, doc.toJson());

    wait(pReply, jsCb);
}

/**
 * @brief CAjax::put  put请求接口
 * @param url 请求地址
 * @param jsObj 请求数据
 * @param jsCb 请求回调
 */
void CAjax::put(QString url, QJSValue jsObj, QJSValue jsCb)
{
    if (url.startsWith("/"))
    {
        url=s_qServerUrl+url;
    }
    QNetworkRequest request=QNetworkRequest(url);
    request.setRawHeader("Content-Type","application/json");

    QJsonDocument doc = QJsonDocument::fromVariant(jsObj.toVariant());
    QNetworkReply *pReply = s_qNetworkManager.put(request, doc.toJson());

    wait(pReply, jsCb);
}

/**
 * @brief CAjax::uploadFile 上传文件
 * @param url 接口地址
 * @param fileObj 文件对象{file1:/a/b/1.txt, file2:/a/b/2.txt}
 * @param jsObj 其他非文件数据{k1:v1, k2:v2},目前提交到后台的参数统一处理为字符串类型
 * @param jsCb 服务器的返回调用
 */
void CAjax::uploadFile(QString url, QJSValue fileObj, QJSValue jsObj, QJSValue jsCb)
{
    if (url.startsWith("/"))
    {
        url=s_qServerUrl+url;
    }
    QNetworkRequest request=QNetworkRequest(url);

    QHttpMultiPart *pMultiPart = new QHttpMultiPart(QHttpMultiPart::FormDataType);

    // 处理文件数据
    QJsonDocument jsonDoc = QJsonDocument::fromVariant(fileObj.toVariant());
    QJsonObject jsonObj=jsonDoc.object();
    for (auto it=jsonObj.begin(); it!=jsonObj.end(); it++)
    {
        QHttpPart imagePart;
        QString loadName=it.key();
        QString fileName=it.value().toVariant().toString();
        QString qStrHeader=QString("form-data; name=\"%1\"; filename=\"%2\"")
                .arg(loadName)
                .arg(QFileInfo(fileName).fileName());
        imagePart.setHeader(QNetworkRequest::ContentDispositionHeader,
                            QVariant(qStrHeader));
        imagePart.setRawHeader("Content-type", "multipart/form-data");
        QFile *pFile = new QFile(fileName, pMultiPart);
        pFile->open(QIODevice::ReadOnly);
        imagePart.setBodyDevice(pFile);
        pMultiPart->append(imagePart);
    }

    // 处理其他json数据
    jsonDoc = QJsonDocument::fromVariant(jsObj.toVariant());
    jsonObj=jsonDoc.object();
    for (auto it=jsonObj.begin(); it!=jsonObj.end(); it++)
    {
        QHttpPart textPart;
        QString key=it.key();
        QVariant value=it.value().toVariant();
        QString qStrHeader=QString("form-data; name=\"%1\"").arg(key);
        textPart.setHeader(QNetworkRequest::ContentDispositionHeader, QVariant(qStrHeader));
        textPart.setBody(value.toByteArray());
        pMultiPart->append(textPart);
    }

    QNetworkReply *pReply = s_qNetworkManager.post(request, pMultiPart);
    pMultiPart->setParent(pReply);

    wait(pReply, jsCb);
}

/**
 * @brief CAjax::wait 等待请求
 * @param pReply
 * @param jsCb
 */
void CAjax::wait(QNetworkReply *pReply, QJSValue jsCb)
{
    QReplyTimeout * pTimeout = new QReplyTimeout(pReply, s_iTimeoutMs);
    Q_UNUSED(pTimeout);

    connect(pReply, &QNetworkReply::finished, [=]()mutable{
        QVariant statusCode = pReply->attribute(QNetworkRequest::HttpStatusCodeAttribute);
        if (statusCode.isValid() && statusCode.toInt()==200)
        {
            QJsonDocument jdoc = QJsonDocument::fromJson(pReply->readAll());
            QJSValue val = jsCb.engine()->toScriptValue(jdoc.toJson());
            QJSValueList vl;
            vl.append(val);
            jsCb.call(vl);
        }
        else
        {
            QString errStr=QString("{\"code\":-1, \"msg\":\"%1\"}").arg(pReply->errorString());
            QJSValue val = jsCb.engine()->toScriptValue(errStr);
            QJSValueList vl;
            vl.append(val);
            jsCb.call(vl);
        }

        pReply->close();
        pReply->deleteLater();
    });
}










