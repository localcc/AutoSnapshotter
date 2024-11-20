import os
import idaapi
import ida_loader
import ida_kernwin

SECOND = 1000
MINUTE = SECOND * 60

# User config
# Interval between snapshots in milliseconds
SNAPSHOT_INTERVAL_MS = 30 * MINUTE
# Amount of snapshots to keep
SNAPSHOT_KEEP_COUNT = 5


def timerElapsed():
    rootSnapshot = ida_loader.snapshot_t()
    ida_loader.build_snapshot_tree(rootSnapshot)

    snapshots = list(rootSnapshot.children)
    snapshots.sort(key=lambda x: x.id)
    snapshots.reverse()

    snapshotsToDelete = snapshots[5:]
    for snapshot in snapshotsToDelete:
        idaapi.msg(
            "Auto-Snapshotter: deleting old snapshot ({}).".format(snapshot.filename)
        )
        os.remove(snapshot.filename)

    newSnapshot = ida_loader.snapshot_t()
    ida_kernwin.take_database_snapshot(newSnapshot)
    idaapi.msg(
        "Auto-Snapshotter: created new snapshot ({})".format(newSnapshot.filename)
    )

    return SNAPSHOT_INTERVAL_MS


ida_kernwin.register_timer(SNAPSHOT_INTERVAL_MS, timerElapsed)
