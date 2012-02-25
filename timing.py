# coding: utf-8
import sys
from subprocess import Popen


ITERATIONS = 10000


def u(value):
    return unicode(value, 'unicode-escape')


def bench_format_literal():
    """u'foobarbaz_%d' % x"""
    for x in xrange(ITERATIONS):
        y = u'foobarbaz_%d' % x


def bench_format_wrapped():
    """u('foobarbaz_%d') % x"""
    for x in xrange(ITERATIONS):
        y = u('foobarbaz_%d') % x


def bench_simple_literal():
    """u'foobarbaz'"""
    for x in xrange(ITERATIONS):
        y = u'foobarbaz'


def bench_simple_wrapped():
    """u('foobarbaz')"""
    for x in xrange(ITERATIONS):
        y = u('foobarbaz')


def bench_non_ascii_literal():
    """u'fööbarbaz'"""
    for x in xrange(ITERATIONS):
        y = u'fööbarbaz'


def bench_non_ascii_wrapped():
    """u('fööbarbaz')"""
    for x in xrange(ITERATIONS):
        y = u('fööbarbaz')


def bench_escaped_literal():
    """u'\N{SNOWMAN}barbaz'"""
    for x in xrange(ITERATIONS):
        y = u'\N{SNOWMAN}barbaz'


def bench_escaped_wrapped():
    """u('\N{SNOWMAN}barbaz')"""
    for x in xrange(ITERATIONS):
        y = u('\N{SNOWMAN}barbaz')


def list_benchmarks():
    for name in sorted(globals().keys()):
        if name.startswith('bench_'):
            yield name[6:]


def run_bench(name):
    text = globals()['bench_' + name].__doc__.strip().decode('utf-8')
    sys.stdout.write((u'%-32s' % text).encode('utf-8'))
    sys.stdout.flush()
    Popen([sys.executable, '-mtimeit', '-s',
           'from timing import bench_%s as run' % name,
           'run()']).wait()


def main():
    print '=' * 80
    print 'Running benchmarks'
    print '-' * 80
    for bench in list_benchmarks():
        run_bench(bench)
    print '-' * 80


if __name__ == '__main__':
    main()
