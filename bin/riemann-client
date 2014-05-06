#!/usr/bin/env python

import sys
import json
import argparse

from datetime import datetime

import bernhard
from bernhard import TCPTransport, UDPTransport


class Riemann(object):

    def __init__(self, host='127.0.0.1', port=5555, protocol='tcp'):

        if protocol == 'tcp':
            transport = TCPTransport
        else:
            transport = UDPTransport

        self.client = bernhard.Client(host=host, port=port, transport=transport)

    def quit(self):

        self.client.disconnect()

    def send(self, event):

        try:
            response = self.client.send(event)
        except Exception, e:
            print >>sys.stderr, str(e)
            sys.exit(1)

        if not response:
            print >>sys.stderr, response

    def query(self, q, format='text'):

        try:
            message = self.client.query(q)
        except Exception, e:
            print >>sys.stderr, str(e)
            sys.exit(1)

        if format == 'json':
            self.dump_events_json(message)
        else:
            self.dump_events(message)

    @staticmethod
    def dump_events(message):

        for n, evt in enumerate(message):
            print ('Event #%s:\n'
                   '  time = %s - %s\n'
                   '  state = %s\n'
                   '  service = %s\n'
                   '  host = %s\n'
                   '  description = %s\n'
                   '  ttl = %s\n'
                   '  metric_sint64 = %s\n'
                   '  metric_d = %s\n'
                   '  metric_f = %s') % (
                        n,
                        evt.time, datetime.fromtimestamp(evt.time).strftime("%c"),
                        evt.state, evt.service, evt.host,
                        evt.description, evt.ttl,
                        evt.metric_sint64, evt.metric_d, evt.metric_f)
            if evt.tags:
                print '  tags = [ %s ]' % ' '.join([str(tag) for tag in evt.tags])
            if evt.attributes:
                print '  attributes = {'
                for attrib in getattr(evt, 'attributes'):
                    print '    %s = %s' % (attrib.key, attrib.value)
                print '  }'

    @staticmethod
    def dump_events_json(message):

        json_object = list()
        for evt in message:
            json_object.append({
                "time": evt.time,
                "state": evt.state,
                "service": evt.service,
                "host": evt.host,
                "description": evt.description,
                "ttl": evt.ttl,
                "metric_sint64": evt.metric_sint64,
                "metric_d": evt.metric_d,
                "metric_f": evt.metric_f,
                "tags": [tag for tag in evt.tags],
                "attributes": dict([(attribute.key, attribute.value) for attribute in event.attributes])
            })
        print json.dumps(json_object)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='riemann-client'
    )
    subparsers = parser.add_subparsers(metavar='COMMAND')

    parser_send = subparsers.add_parser('send')
    parser_send.add_argument(
        '-s',
        '--state',
        help='Set the state of the event.'
    )
    parser_send.add_argument(
        '-S',
        '--service',
        help='Set the service sending the event.'
    )
    parser_send.add_argument(
        '-H',
        '--host',
        help='Set the origin host of the event.'
    )
    parser_send.add_argument(
        '-D',
        '--description',
        help='Set the description of the event.'
    )
    parser_send.add_argument(
        '-a',
        '--attribute',
        action='append',
        metavar='KEY=VALUE',
        help='Add a new attribute to the event.'
    )
    parser_send.add_argument(
        '-t',
        '--tag',
        action='append',
        help='Add a tag to the event.'
    )
    parser_send.add_argument(
        '-i',
        '--metric-sint64',
        type=int,
        metavar='METRIC',
        help='Set the 64bit integer metric of the event.'
    )
    parser_send.add_argument(
        '-d',
        '--metric-d',
        type=int,
        metavar='METRIC',
        help='Set the double metric of the event.'
    )
    parser_send.add_argument(
        '-f',
        '--metric-f',
        type=float,
        metavar='METRIC',
        help='Set the float metric of the event.'
    )
    parser_send.add_argument(
        '-L',
        '--ttl',
        type=int,
        help='Set the TTL of the event.'
    )
    parser_send.add_argument(
        '-T',
        '--tcp',
        action='store_const',
        dest='protocosl',
        const='tcp',
        #default='tcp',
        help='Send the message over TCP (default).'
    )
    parser_send.add_argument(
        '-U',
        '--udp',
        action='store_const',
        dest='protocol',
        const='udp',
        default='tcp',
        help='Send the message over UDP.'
    )
    parser_send.add_argument(
        'host',
        nargs='?',
        default='localhost'
    )
    parser_send.add_argument(
        'port',
        type=int,
        nargs='?',
        default=5555
    )

    parser_query = subparsers.add_parser('query')
    parser_query.add_argument('query')
    parser_query.add_argument(
        '-j',
        '--json',
        action='store_true',
        help='Output the results as a JSON array.'
    )
    parser_query.add_argument(
        'host',
        nargs='?',
        default='localhost'
    )
    parser_query.add_argument(
        'port',
        type=int,
        nargs='?',
        default=5555
    )
    args = parser.parse_args()

    client = Riemann(host=args.host, port=args.port, protocol=getattr(args, 'protocol', 'tcp'))

    if hasattr(args, 'query'):
        fmt = 'json' if args.json else 'text'
        try:
            client.query(args.query, fmt)
        except (SystemExit, KeyboardInterrupt):
            sys.exit(0)
    else:
        event = dict()
        if args.state:
            event['state'] = args.state
        if args.service:
            event['service'] = args.service
        if args.host:
            event['host'] = args.host
        if args.description:
            event['description'] = args.description
        if args.ttl:
            event['ttl'] = args.ttl
        if args.metric_sint64:
            event['metric_sint64'] = args.metric_sint64
        if args.metric_d:
            event['metric_d'] = args.metric_d
        if args.metric_f:
            event['metric_f'] = args.metric_f
        if args.tag:
            event['tags'] = args.tag
        if args.attribute:
            event['attributes'] = dict([attribute.split('=') for attribute in args.attribute])

        try:
            client.send(event)
        except (SystemExit, KeyboardInterrupt):
            sys.exit(0)

    client.quit()
