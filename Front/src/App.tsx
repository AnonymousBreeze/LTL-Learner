import { QuestionCircleOutlined } from '@ant-design/icons'
import { Button, Popover } from 'antd'
import { useEffect, useState } from 'react';
import { NaturalConvert } from './components/NaturalConvert/NaturalConvert';
import { DocumentConvert } from './components/DocumentConvert/DocumentConvert';
import { E_LOCAL_KEY, I_CONVERT_CONFIGURATION } from './interface/localStorageKey';
import { E_MODEL, E_PROMPT_TYPE } from './interface/converConfiguration';

function App() {
  const [selected, setSelected] = useState<string>('natural');

  useEffect(() => {
    localStorage.setItem(E_LOCAL_KEY.NATURAL_HISTORY, localStorage.getItem(E_LOCAL_KEY.NATURAL_HISTORY) ?? '[]')

    localStorage.setItem(E_LOCAL_KEY.CONVERT_CONFIGURATION,
      localStorage.getItem(E_LOCAL_KEY.CONVERT_CONFIGURATION) ?? JSON.stringify({
        model: E_MODEL.GPT35,
        promptType: E_PROMPT_TYPE.dynamic,
        temperature: 0
      } as I_CONVERT_CONFIGURATION)
    )
  }, [])

  return (
    <>
      <div className="flex items-center justify-between border-b border-solid border-gray-200 p-3 px-8 shadow-md">
        <div className="flex items-center gap-2">
          <div className="cursor-default">Convert to LTL</div>
          <Popover content="Translating Unstructured Natural Language to Lineal Temporal Logics">
            <QuestionCircleOutlined className='cursor-pointer' />
          </Popover>
        </div>
        <div className="flex items-center gap-2">
          <div className="cursor-pointer p-2 rounded-md hover:bg-[#f5f5f5] ">About</div>
        </div>
      </div>

      <div className="m-auto min-w-[960px] p-6 text-base mx-20">
        <div className="flex gap-3">
          <Button
            onClick={() => {
              setSelected('natural')
            }}
            className={`flex items-center gap-2 text-base py-1 h-max ${selected === 'natural' ? 'border-blue-400 text-blue-400' : ''}`}
          >
            <i className='iconfont icon-ziranyuyanchuli' style={{ fontSize: '20px' }} />Natural Language
          </Button>
          <Button
            className={`flex items-center gap-2 text-base  py-1 h-max ${selected === 'document' ? 'border-blue-400 text-blue-400' : ''}`}
            onClick={() => {
              setSelected('document')
            }}
          >
            <i className='iconfont icon-xlsx' style={{ fontSize: '20px' }} />Batch Translation
          </Button>
        </div>

        {selected === "natural" &&
          <NaturalConvert />
        }


        {selected === "document" &&
          <DocumentConvert />
        }
      </div>
    </>
  )
}

export default App
