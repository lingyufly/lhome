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

    Q_INVOKABLE void remove(const QString &key);
    Q_INVOKABLE bool contains(const QString &key) const;

};

#endif // CSETTINGS_H
