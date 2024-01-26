import { Col, Drawer, Popover, Row } from 'antd'
import { useEffect, useState } from 'react'
import { E_LOCAL_KEY, I_CONVERT_HISTORY } from '../../interface/localStorageKey';
type IProps = {
    show: boolean,
    onFinish: () => void,
    localKey: string
}

export function ConvertHistory(props: IProps) {
    const { show = false, onFinish = () => { setOpen(false) }, localKey = E_LOCAL_KEY.NATURAL_HISTORY } = props;
    const [open, setOpen] = useState<boolean>(false);
    const [history, setHistory] = useState<I_CONVERT_HISTORY[]>([]);

    useEffect(() => {
        setOpen(show);
    }, [props, show]);

    useEffect(() => {
        if (open) {
            const localHistory = JSON.parse(localStorage.getItem(localKey) ?? '[]');
            setHistory(localHistory);
        }
    }, [props, localKey, open])

    const onClose = () => {
        onFinish();
    };

    return (
        <Drawer title="Translation History" placement="right" width={760} onClose={onClose} open={open}>
            <div className="flex flex-col divide-y border border-solid border-gray-200">
                <Row className='p-0 divide-x'>
                    <Col className='p-2 flex items-center justify-center' span={6}>Date</Col>
                    <Col className='p-2 flex items-center justify-center truncate' span={9}>Natural Language</Col>
                    <Col className='p-2 flex items-center justify-center truncate' span={9}>Linear Temporal Logic</Col>
                </Row>

                {history.map(item => {
                    return <Row className='p-0 divide-x'>
                        <Col className='p-2 flex items-center justify-center' span={6} > {item.date}</Col>
                        <Col className='p-2 flex items-center justify-center' span={9}><Popover content={item.source}><div className="w-full truncate text-center">{item.source}</div></Popover></Col>
                        <Col className='p-2 flex items-center justify-center truncate' span={9}><Popover content={item.source}><div className="w-full truncate text-center">{item.result}</div></Popover></Col>
                    </Row>

                })}
            </div >
        </Drawer >
    )
}
