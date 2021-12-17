#ifndef CSETTINGS_H
#define CSETTINGS_H

#include <QSettings>

class CSettings : public QSettings
{
    Q_OBJECT

public:
    explicit CSettings(const QString &organization,
                       const QString &application = QString(), QObject *parent = nullptr);
    CSettings(Scope scope, const QString &organization,
              const QString &application = QString(), QObject *parent = nullptr);
    CSettings(Format format, Scope scope, const QString &organization,
              const QString &application = QString(), QObject *parent = nullptr);
    CSettings(const QString &fileName, Format format, QObject *parent = nullptr);
    explicit CSettings(QObject *parent = nullptr);

    virtual ~CSettings();

    Q_INVOKABLE void setValue(const QString &key, const QVariant &value);
    Q_INVOKABLE QVariant value(const QString &key, const QVariant &defaultValue = QVariant()) const;

    Q_INVOKABLE bool getBool(const QString &key, bool defaultValue=false) const;
    Q_INVOKABLE int getInt(const QString &key, int defaultValue=0) const;
    Q_INVOKABLE double getDouble(const QString &key, double defaultValue=0.0) const;
    Q_INVOKABLE QString getString(const QString &key, QString defaultValue="") const;

    Q_INVOKABLE void remove(const QString &key);
    Q_INVOKABLE bool contains(const QString &key) const;

};

#endif // CSETTINGS_H
