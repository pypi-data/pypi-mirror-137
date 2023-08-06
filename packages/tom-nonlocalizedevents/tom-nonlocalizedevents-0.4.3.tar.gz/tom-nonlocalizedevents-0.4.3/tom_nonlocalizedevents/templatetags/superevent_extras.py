from dateutil.parser import parse

from django import template

register = template.Library()


@register.filter
def percentage_filter(value):
    """
    Converts a decimal to a percentage with a single decimal place.
    """
    try:
        return f"{'%.1f' % (float(value) * 100)}%"
    except Exception:
        print(f'exception: {value}')
        return value


@register.inclusion_tag('tom_nonlocalizedevents/partials/alert_table.html', takes_context=True)
def alert_table(context):
    """
    Displays the alerts of an event.
    """
    alerts = [{'url': f'http://skip.dev.hop.scimma.org/api/v2/alerts/{alert["id"]}/',
               'identifier': f'GCN {alert["identifier"]}',
               'timestamp': str(parse(alert['timestamp']).date()),
               'from': alert['parsed_message']['from'].split(' at ', 1)[0],
               'subject': alert['parsed_message']['subject'].split(':', 1)[-1]
               } for alert in context['superevent_data']['alerts'][:8]
              if alert['parsed_message'].get('title', None) != 'GCN/LVC NOTICE']
    superevent_alert = None
    for alert in context['superevent_data']['alerts']:
        if alert['parsed_message'].get('title', None) == 'GCN/LVC NOTICE':
            superevent_alert = alert
            superevent_alert['timestamp'] = str(parse(superevent_alert['timestamp']).date())
            superevent_alert['url'] = context['superevent_data']['url']
            break

    return {
        'alerts': alerts,
        'superevent_alert': superevent_alert
    }
