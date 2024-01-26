/**
 * 枚举工具类
 *
 * @export
 * @class EnumHelpers
 */
export class EnumHelpers {
  /**
   * 格式化枚举为list
   *
   * @static
   * @param {*} enumObject
   * @memberof EnumHelpers
   */
  static ToArray<T = any>(
    enumObject: any
  ): {
    label: string;
    value: T;
  }[] {
    const keys = Object.keys(enumObject);

    if (keys.some((value) => Number(value))) {
      return keys
        .filter((value) => isNaN(Number(value)) === false)
        .map((key) => {
          return {
            label: enumObject[key],
            value: Number(key) as any
          };
        });
    } else {
      return keys.map((key) => {
        return { label: key, value: enumObject[key] as T };
      });
    }
  }

  /**
   * 格式化枚举为map
   *
   * @static
   * @param {*} enumObject
   * @return {*}  {Record<any, any>}
   * @memberof EnumHelpers
   */
  static toValueKeyMap(enumObject: any): Record<any, any> {
    const keys = Object.keys(enumObject);
    const res: Record<any, any> = {};
    keys.forEach((key) => {
      const val = enumObject[key];
      res[val] = key;
    });
    return res;
  }
}
