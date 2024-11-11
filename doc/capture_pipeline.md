# Capture Pipeline

## Get video frames

The capture pipeline uses the XDG desktop portal to get
a filehandle for a stream of video frames.

When interacting with the portal asynchronous messages
are sent over D-Bus.

Once the filehandle has been obtained ("source started"),
the filehandle is used with a Gstreamer pipleline ("parse
launch") to get the video frames.

Every video frame is received by a callback ("on buffer")
where the dominant color is determined and the frame is
converted to an image.  Both dominant color and frame image
are made available to the application using Qt's signal and
slot mechanism.

```mermaid
sequenceDiagram
    participant C as CapturePipeline
    participant D as DBus
    C ->> D: get portal
    create participant P as Portal
    D -->> P: create proxy
    C -) P: create session
    P ->>+ C: session created
    C -)- P: select sources
    P ->>+ C: sources selected
    C -)- P: start
    P ->>+ C: source started
    C ->> C: start pipewire stream
    participant G as GStreamer
    C -) G: parse launch
    deactivate C
    loop on every frame
    G ->> C: on buffer
    activate C
    C --> C: emit signals
    deactivate C
    end
```

# GStreamer Pipeline

The GST pipeline receives the stream of video frames.
It limits the framerate to something manageable, and
downscales the image to a smaller size for more efficient
processing.  Finally the frame is sent to the Python callback.

```mermaid
flowchart TB
    pipewiresrc --> videorate --> videoconvert --> videoscale --> v["specify RGB 160x80"] --> appsink
```

