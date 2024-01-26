import NiceModal, { useModal } from '@ebay/nice-modal-react'
import { Col, Input, Modal, Popover, Row, message } from 'antd';
import TextArea from 'antd/es/input/TextArea';
import { useCallback, useState } from 'react';
import _ from 'lodash';
import { instance } from '../../services/base';

interface Rule {
    sub_expression: string;
    ltl_formula: string;
}

export const EditRule = NiceModal.create((props: { currentNL: string }) => {
    const { currentNL } = props;
    const modal = useModal();
    const [value, setValue] = useState<string>(''); // 预期的LTL结果
    const [ruleArr, setRuleArr] = useState<Rule[]>([]); // 添加的规则

    const handleAddRule = () => {
        const newRules = _.cloneDeep(ruleArr);
        newRules.push({ sub_expression: '', ltl_formula: '' });
        setRuleArr(newRules);
    };

    const handleInputChange = (value: string, field: keyof Rule, index: number) => {
        const newRules = ruleArr.map((item, i) =>
            i === index ? { ...item, [field]: value } : item
        );
        setRuleArr(newRules);
    };

    const handleDeleteRule = (index: number) => {
        const newRules = [...ruleArr];
        newRules.splice(index, 1);
        setRuleArr(newRules);
    };

    const onOk = useCallback(async () => {
        const ruleJson: Rule[] = [];
        ruleJson.push({
            "sub_expression": currentNL,
            "ltl_formula": value
        }, ...ruleArr)

        const param = {
            nl: currentNL,
            rule: ruleJson
        }
        try {
            await instance.post('/submit_new_prompt', param, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            message.success('Add Rule Success!');
            modal.hide();
        } catch {
            message.error('Unknown exception!')
        }
    }, [currentNL, modal, ruleArr, value])

    return (
        <Modal title="Optimizing Prompt" width={750} open={modal.visible} onCancel={modal.hide} onOk={onOk} afterClose={modal.remove}>
            <div className="flex flex-col gap-2 mt-6">
                <div className="flex items-center"> 
                    <p className="font-bold w-max whitespace-nowrap">Current Natural Language： </p>
                    <Popover content={currentNL}>
                        <p className=" truncate">{currentNL}</p>
                    </Popover>
                </div>
                <div className="">
                    <p className="font-bold w-max whitespace-nowrap">Expected LTL results:</p>
                    <TextArea rows={4} cols={1} value={value} onChange={(e) => { setValue(e.target.value) }} placeholder="Enter the expected Lineal Temporal Logics results." maxLength={99} />
                </div>

                <div className="flex flex-col gap-2">
                    <div className="flex justify-between">
                        <p className="font-bold w-max whitespace-nowrap">Add New Rule</p>
                        <Popover content="Add Rule">
                            <p className='border border-solid border-gray-300 px-4 hover:bg-gray-300 cursor-pointer'
                                onClick={handleAddRule}
                            >+</p>
                        </Popover>
                    </div>
                    <Row>
                        <Col span={11} className='text-center'>Sub_expression</Col>
                        <Col span={11} className='text-center'>LTL_Formula</Col>
                        <Col span={2}>
                            {/* <Button danger type="default">删除</Button> */}
                        </Col>
                    </Row>
                    {ruleArr.map((item, index) => {
                        return <Row key={index} gutter={[50, 1000]}>
                            <Col span={10}><Input value={item.sub_expression} onChange={(e) => handleInputChange(e.target.value, 'sub_expression', index)} /></Col>
                            <Col span={10}><Input value={item.ltl_formula} onChange={(e) => handleInputChange(e.target.value, 'ltl_formula', index)} /></Col>
                            <Col span={4} className='flex items-center justify-center'>
                                <p className='w-max flex items-center justify-center border border-solid text-red-500 border-red-500 px-4 hover:bg-red-500 hover:text-white cursor-pointer'
                                    onClick={() => handleDeleteRule(index)}
                                >delete</p>
                            </Col>
                        </Row>
                    })}
                </div>

            </div>
        </Modal>
    )
})
