import React, { useRef, useEffect, useState } from 'react';

const WebcamComponent = () => {
    const videoRef = useRef(null);
    const [isCameraOn, setIsCameraOn] = useState(false);
    const [stream, setStream] = useState(null);
    const [processedImage, setProcessedImage] = useState(null);

    const startCamera = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                setStream(stream);
            }
            setIsCameraOn(true);
        } catch (err) {
            console.error("Error accessing webcam: ", err);
        }
    };

    const stopCamera = () => {
        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        setIsCameraOn(false);
    };

    const sendFrameToServer = async (frame) => {
        try {
            const response = await fetch('http://127.0.0.1:8080/data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ frame })
            });
            const data = await response.json();
            setProcessedImage(`data:image/jpeg;base64,${data.processed_image}`);
        } catch (err) {
            console.error("Error sending frame to server: ", err);
        }
    };

    useEffect(() => {
        if (isCameraOn && videoRef.current) {
            const interval = setInterval(() => {
                const canvas = document.createElement('canvas');
                canvas.width = videoRef.current.videoWidth;
                canvas.height = videoRef.current.videoHeight;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
                const frame = canvas.toDataURL('image/jpeg');
                sendFrameToServer(frame);
            }, 1000); // 1초마다 프레임 전송

            return () => clearInterval(interval);
        }
    }, [isCameraOn]);

    useEffect(() => {
        return () => {
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        };
    }, [stream]);

    const saveImage = () => {
        if (processedImage) {
            const link = document.createElement('a');
            link.href = processedImage;
            link.download = 'processed_image.jpg';
            link.click();
        }
    };

    return (
        <>
            <h1>Webcam 화면</h1>
            <div>
                <button onClick={isCameraOn ? stopCamera : startCamera}>
                    {isCameraOn ? '카메라 끄기' : '카메라 켜기'}
                </button>
                <button onClick={saveImage} disabled={!processedImage}>
                    사진 저장
                </button>
            </div>
            <div style={{ display: "flex" }}>
                <video ref={videoRef} autoPlay playsInline />
                <div>
                    {processedImage && <img src={processedImage} alt="Processed" />}
                </div>
            </div>
        </>
    );
};

export default WebcamComponent;
