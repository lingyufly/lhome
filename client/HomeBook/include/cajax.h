/*************************************************************************
  > File Name:      cajax.h
  > Author:         ly
  > Created Time:   Sat 23 Oct 2021 09:43:53 PM CST
  > Description:    封装的http请求接口
 ************************************************************************/


#ifndef _CAJAX_H_
#define _CAJAX_H_

#include <QObject>
#include <QJSValue>
#include <QVariant>

class QNetworkAccessManager;
class QNetworkReply;
class QTimer;

class QReplyTimeout : public QObject
{
    Q_OBJECT
public:
    explicit QReplyTimeout(QNetworkReply *parent,int timeout);
    virtual ~QReplyTimeout();

private:
    QTimer* mTimeoutTimer;
};


class CAjax:public QObject
{
  Q_OBJECT
public:
    explicit CAjax(QObject *parent=0);
    virtual ~CAjax();

    Q_INVOKABLE static void setServerUrl(QString url);
    Q_INVOKABLE static void setTimeout(int iMs);

    Q_INVOKABLE void get(QString url, QJSValue jsObj, QJSValue jsCb);
    Q_INVOKABLE void post(QString url, QJSValue jsObj, QJSValue jsCb);
    Q_INVOKABLE void put(QString url, QJSValue jsObj, QJSValue jsCb);

    Q_INVOKABLE void uploadFile(QString url, QJSValue fileObj, QJSValue jsObj, QJSValue jsCb);

protected slots:

protected:
    void wait(QNetworkReply *pReply, QJSValue jsCb);

private:
    static QNetworkAccessManager s_qNetworkManager;
    static QString s_qServerUrl;
    static int s_iTimeoutMs;
};


#endif // AJAX_H
