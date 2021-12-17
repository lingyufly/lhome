/*************************************************************************
  > File Name:      csettings.cpp
  > Author:         ly
  > Created Time:   Sat 23 Oct 2021 09:43:53 PM CST
  > Description:    
 ************************************************************************/

#include <iostream>
#include <QDebug>

#include "csettings.h"

CSettings::CSettings(const QString &organization,
                   const QString &application, QObject *parent)
    :QSettings(organization, application, parent)
{

}
CSettings::CSettings(Scope scope, const QString &organization,
          const QString &application, QObject *parent)
    :QSettings(scope, organization, application, parent)
{

}
CSettings::CSettings(Format format, Scope scope, const QString &organization,
          const QString &application, QObject *parent)
    :QSettings(format, scope, organization, application, parent)
{

}
CSettings::CSettings(const QString &fileName, Format format, QObject *parent)
    :QSettings(fileName, format, parent)
{

}
CSettings::CSettings(QObject *parent)
    :QSettings(parent)
{

}

CSettings::~CSettings()
{

}

void CSettings::setValue(const QString &key, const QVariant &value)
{
    QSettings::setValue(key, value);
}
QVariant CSettings::value(const QString &key, const QVariant &defaultValue) const
{
    QVariant qvar=QSettings::value(key, defaultValue);
    return qvar;
}

bool CSettings::getBool(const QString &key, bool defaultValue) const
{
    QVariant qvar=QSettings::value(key, defaultValue);

    return qvar.toBool();
}

int CSettings::getInt(const QString &key, int defaultValue) const
{
    QVariant qvar=QSettings::value(key, defaultValue);

    return qvar.toInt();
}

double CSettings::getDouble(const QString &key, double defaultValue) const
{
    QVariant qvar=QSettings::value(key, defaultValue);

    return qvar.toDouble();
}

QString CSettings::getString(const QString &key, QString defaultValue) const
{
    QVariant qvar=QSettings::value(key, defaultValue);

    return qvar.toString();
}

void CSettings::remove(const QString &key)
{
    QSettings::remove(key);
}
bool CSettings::contains(const QString &key) const
{
    return QSettings::contains(key);
}



