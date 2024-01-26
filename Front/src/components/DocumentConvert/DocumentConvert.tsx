import { InboxOutlined, LoadingOutlined } from '@ant-design/icons'
import { Button, Col, Row, Upload, message } from 'antd';
import { RcFile, UploadChangeParam, UploadFile } from 'antd/es/upload';
import Dragger, { DraggerProps } from 'antd/es/upload/Dragger'
import { useCallback, useMemo, useState } from 'react'
import { instance } from '../../services/base';
import { downloadFile } from '../../utils/download';
import xlsxPng from "../../assets/icons/xlsx.png"
import "./documentConvert.css"

export function DocumentConvert() {
    const [loading, setLoading] = useState<boolean>(false);
    const [result, setResult] = useState<Blob>();
    const [uploadFile, setUploadFile] = useState<string | Blob | RcFile>();

    const onOk = useCallback(async () => {
        if (uploadFile) {
            setLoading(true);
            try {
                const formData = new FormData();
                formData.append('excelFile', uploadFile);
                const resultFile = await instance.post('/batch_translate', formData, {
                    responseType: 'blob', // 设置响应类型为 Blob
                })
                setResult(resultFile.data as Blob);
            } catch {
                message.error('Unknown exception!')
            }
            setLoading(false);
        } else {
            message.warning('Please upload the file first.')
        }
    }, [uploadFile])

    // 文件上传配置项
    const fileProps: DraggerProps = useMemo(
        () => ({
            name: 'file',
            maxCount: 1,
            multiple: true,
            defaultFileList: [],
            // 自定义请求过程
            async customRequest({ file, onSuccess }) {
                setUploadFile(file);
                if (onSuccess) {
                    onSuccess(file);
                }
            },

            /**
             * 此处逻辑用来过滤文件类型
             *
             * @param {*} info
             * @return {*}
             */
            beforeUpload(info) {
                return new Promise((resolve) => {
                    const isDocx = /\.(xlsx)$/.test(info.name);
                    if (isDocx) {
                        resolve(info);
                        return true;
                    } else {
                        // setHtmlString('');
                        message.warning('File format error!');
                        // reject(info);
                        return Upload.LIST_IGNORE;
                    }
                })
            },
            // 上传文件变动
            onChange(info: UploadChangeParam<UploadFile<unknown>>) {
                const { status } = info.file;
                if (status === 'done') {
                    message.success(`Uploaded file: ${info.file.name}`);
                } else if (status === 'error') {
                    message.warning(`${info.file.name} file upload failed.`);
                }
            },
            // 删除上传文件
            onDrop(e) {
                console.log('Dropped files', e.dataTransfer.files);
            }
        }),
        []
    );
    return (
        <div className="mt-6 flex flex-col items-center">
            <Row className='w-full h-60'>
                <Col span={10} className='h-full'>
                    <div className="col-span-5 h-full">
                        <Dragger {...fileProps}>
                            <p className="ant-upload-drag-icon pt-10">
                                <InboxOutlined />
                            </p>
                            <div className="ant-upload-text"><div className="text-2xl">Upload xlsx files to be translated.</div></div>
                        </Dragger>
                    </div>
                </Col>

                <Col span={4} className='flex items-center justify-center'>
                    <Button type="dashed" className='h-max'
                        onClick={onOk}
                    >
                        <div className="flex items-center text-base">Convert --&gt;</div>
                    </Button>
                </Col>

                <Col span={10}>
                    <div className="col-span-5 text-2xl h-full rounded-md overflow-y-auto bg-gray-100 p-2">
                        {!loading && !result && <div className="text-gray-500">Lineal Temporal Logics Result File</div>}
                        {(loading || result) && <div className="mt-8 flex flex-col items-center justify-center">
                            <img width={50} src={xlsxPng} />
                            {!loading &&
                                <p
                                    className='text-blue-500 hover:text-blue-400 cursor-pointer'
                                    onClick={() => {
                                        if (result) {
                                            downloadFile(result, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'convertResult.xlsx')
                                        }
                                    }}>
                                    Click to download
                                </p>
                            }

                            {loading &&
                                <>
                                    <LoadingOutlined style={{ fontSize: 14 }} spin />
                                    <p>Converting...</p>
                                </>
                            }
                        </div>}
                    </div>
                </Col>
            </Row>

        </div >
    )
}
