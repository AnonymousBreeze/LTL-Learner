import NiceModal, { useModal } from '@ebay/nice-modal-react'
import { Col, InputNumber, Modal, Row, Select, Slider } from 'antd'
import { useEffect, useState } from 'react'
import { EnumHelpers } from '../../utils/EnumHelper';
import { E_LOCAL_KEY, I_CONVERT_CONFIGURATION } from '../../interface/localStorageKey';


enum E_MODEL {
    GPT35 = 'GPT35',
    GPT4 = 'GPT4',
    Gemini = 'Gemini',
}
enum E_PROMPT_TYPE {
    dynamic = 'dynamic',
    static = 'static',
    zeroShot = 'zero-shot',
}


export const ConvertConfiguration = NiceModal.create(() => {
    const modal = useModal();

    const [modelValue, setModelValue] = useState<E_MODEL>(E_MODEL.GPT35);
    const [promptValue, setPromptValueValue] = useState<E_PROMPT_TYPE>(E_PROMPT_TYPE.dynamic);
    const [temperatureValue, setTemperatureValue] = useState<number>(0);

    useEffect(() => {
        const localConfig = localStorage.getItem(E_LOCAL_KEY.CONVERT_CONFIGURATION);
        if (localConfig) {
            const config: I_CONVERT_CONFIGURATION = JSON.parse(localConfig);
            setModelValue(config.model);
            setPromptValueValue(config.promptType);
            setTemperatureValue(config.temperature);
        }
    }, [])


    const onOk = () => {
        const localConfig: I_CONVERT_CONFIGURATION = {
            model: modelValue,
            promptType: promptValue,
            temperature: temperatureValue
        }
        localStorage.setItem(E_LOCAL_KEY.CONVERT_CONFIGURATION, JSON.stringify(localConfig))
        modal.hide();
    }

    return (
        <Modal title="Convert Configuration" onCancel={modal.hide} afterClose={modal.remove} onOk={onOk} open={modal.visible}>
            <div className="flex flex-col gap-3 mt-5">
                <Row align={'middle'}>
                    <Col span={6}>Model</Col>
                    <Col span={6}>
                        <Select className='w-40' value={modelValue} onChange={setModelValue}>
                            {EnumHelpers.ToArray(E_MODEL).map(item => {
                                return <Select.Option value={item.value}>{item.label}</Select.Option>
                            })}
                        </Select>
                    </Col>
                </Row>
                <Row align={'middle'}>
                    <Col span={6}>Prompt Type</Col>
                    <Col span={6}>
                        <Select className='w-40' value={promptValue} onChange={setPromptValueValue}>
                            {EnumHelpers.ToArray(E_PROMPT_TYPE).map(item => {
                                return <Select.Option value={item.value}>{item.label}</Select.Option>
                            })}
                        </Select>
                    </Col>
                </Row>
                <Row align={'middle'}>
                    <Col span={6}>Temperature</Col>
                    <Col span={12}>
                        <Slider
                            min={0}
                            max={1}
                            step={0.01}
                            onChange={setTemperatureValue}
                            value={typeof temperatureValue === 'number' ? temperatureValue : 0}
                        />
                    </Col>
                    <Col span={4}>
                        <InputNumber
                            min={0}
                            max={1}
                            step={0.01}
                            style={{ margin: '0 16px' }}
                            value={temperatureValue}
                            onChange={(value) => {
                                setTemperatureValue(value ?? 0)
                            }}
                        />
                    </Col>
                </Row>
            </div>
        </Modal>
    )
})
