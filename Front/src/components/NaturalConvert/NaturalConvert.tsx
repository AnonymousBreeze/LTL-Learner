import { Button, Col, Popover, Row, message } from 'antd'
import TextArea from 'antd/es/input/TextArea'
import { useState } from 'react'
import { instance } from '../../services/base'
import { LoadingOutlined, SettingOutlined } from '@ant-design/icons'
import { ConvertHistory } from '../ConvertHistory/ConvertHistory'
import dayjs from 'dayjs'
import NiceModal from '@ebay/nice-modal-react'
import { EditRule } from '../EditRule/EditRule'
import { ConvertConfiguration } from '../ConvertConfiguration/ConvertConfiguration'
import { E_LOCAL_KEY, I_CONVERT_CONFIGURATION, I_CONVERT_HISTORY } from '../../interface/localStorageKey'

export function NaturalConvert() {
    const [value, setValue] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(false)
    const [result, setResult] = useState<string>('');
    const [open, setOpen] = useState<boolean>(false);

    return (
        <div className="mt-6 flex flex-col items-center">
            <Row className='w-full'>
                <Col span={10}>
                    <TextArea className='text-2xl' rows={6} cols={1} value={value} onChange={(e) => { setValue(e.target.value) }} placeholder="Please enter the natural language you want to process." maxLength={9999} />
                </Col>

                <Col span={4} className='flex items-center justify-center relative'>
                    <Popover content="Convert Configuration">
                        <SettingOutlined className="absolute top-12 cursor-pointer hover:text-blue-500 text-lg" onClick={() => { NiceModal.show(ConvertConfiguration) }} />
                    </Popover>
                    <Button type="dashed" className='h-max'
                        onClick={async () => {
                            if (value.length <= 0) {
                                message.warning('The input item cannot be empty.')
                            } else {
                                setLoading(true);
                                try {
                                    const localConfig = localStorage.getItem(E_LOCAL_KEY.CONVERT_CONFIGURATION);
                                    if (localConfig) {
                                        const config: I_CONVERT_CONFIGURATION = JSON.parse(localConfig)
                                        const result = await instance.post('/convert_nl_to_ltl', {
                                            nlInput: value,
                                            model: config.model,
                                            prompt_type: config.promptType,
                                            temperature: config.temperature
                                        })
                                        setResult(result.data.ltlResult);
                                        // 更新历史记录
                                        const storageNatural = JSON.parse(localStorage.getItem(E_LOCAL_KEY.NATURAL_HISTORY) ?? '[]') as I_CONVERT_HISTORY[];
                                        storageNatural.unshift({
                                            date: dayjs().format("YYYY-MM-DD HH:mm:ss"),
                                            source: value,
                                            result: result.data.ltlResult
                                        })
                                        localStorage.setItem(E_LOCAL_KEY.NATURAL_HISTORY, JSON.stringify(storageNatural.slice(0, 10)))
                                    }
                                } catch {
                                    message.error('Unknown exception!')
                                }
                                setLoading(false);
                            }
                        }}
                    >
                        <div className="flex items-center text-base">Convert --&gt;{loading && <LoadingOutlined />}</div>
                    </Button>

                    <Popover content="History">
                        <div className="w-12 h-12 absolute bottom-6 cursor-pointer hover:text-blue-500 rounded-full border border-solid flex items-center justify-center hover:border-blue-300" onClick={() => { setOpen(true) }}><i className='iconfont icon-lishi' style={{ fontSize: "36px", translate: '0 -2px' }}></i></div>
                    </Popover>
                </Col>
                <Col span={10}>
                    <div className="col-span-5 text-2xl h-full rounded-md overflow-y-auto bg-gray-100 py-2 px-3 wrap" style={{ overflowWrap: "anywhere" }}>
                        {!result && <div className="text-gray-500">Lineal Temporal Logics Result</div>}
                        {result}
                    </div>
                    {result && <p
                        className='ml-auto w-max mt-1 border border-solid text-red-500 border-red-500 px-4 hover:bg-red-500 hover:text-white cursor-pointer'
                        onClick={() => {
                            NiceModal.show(EditRule, { currentNL: value })
                        }}
                    >
                        Result Error?
                    </p>
                    }
                </Col>
            </Row>

            {/* <div className="flex flex-col items-center justify-center gap-2 cursor-pointer hover:text-blue-500 group">
                <div className="w-24 h-24 mt-40 rounded-full border border-solid flex items-center justify-center group-hover:border-blue-300" onClick={() => { setOpen(true) }}><i className='iconfont icon-lishi' style={{ fontSize: "36px", translate: '0 -2px' }}></i></div>
                <div className="">History</div>
            </div> */}

            <ConvertHistory show={open} onFinish={() => { setOpen(false) }} localKey={E_LOCAL_KEY.NATURAL_HISTORY} />
        </div >
    )
}
